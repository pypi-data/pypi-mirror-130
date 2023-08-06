"""
Creates the dashboard as a webpage via flask, using the data passed in from other modules.

Functions:
    schedule_update()
    run_scheduled_update()
    remove_update_from_update_list()
    get_event_update_name()
    web_interface()
"""

import sched
import time
import logging

from flask import Flask, render_template, request

from hjc236_covid_dashboard.covid_data_handler import covid_API_request, update_covid
from hjc236_covid_dashboard.covid_news_handling import news_API_request, update_news, format_news_data
from hjc236_covid_dashboard.time_conversions import hhmm_to_seconds, current_time_seconds
from hjc236_covid_dashboard.config_handler import get_config_data, validate_config_data

log_file_location = get_config_data()["log_file_path"]
logging.basicConfig(filename=log_file_location, level=logging.DEBUG, format="%(asctime)s %(message)s")

app = Flask(__name__)
web_scheduler = sched.scheduler(time.time, time.sleep)

# On startup, ensure that the values in the configuration file are valid
config_data = get_config_data()
validate_config_data(config_data)

# Initialise news articles
logging.info("Initialising news articles")
webpage_news_articles = format_news_data(news_API_request())
deleted_articles = []

# Initialise COVID data
logging.info("Initialising COVID data")
webpage_covid_data = covid_API_request()

# Create updates list which contains the updates displayed on the left webpage sidebar
updates = []


def schedule_update(update_time: str, update_name: str, repeat=False, covid=False, news=False) -> None:
    """Takes in the update time in seconds and schedules an update for that time, repeating if necessary. Both,
    or one of, covid data and news data can be updated. If neither are updated, ignore the update and warn user."""

    # If user schedules an update without news or covid, ignore it and warn them there is nothing to update
    if not (covid or news):
        logging.warning("Empty update attempted, ignoring. Updates must update at least one of Covid data or news.")
        return

    for update in updates:
        if update["title"] == update_name:
            logging.warning(f"Error: there is already an update called {update_name}, update names must be unique")
            return

    update_time_hhmm = update_time
    update_time = hhmm_to_seconds(update_time)

    # First, work out the requested time for the first update to happen (how many seconds away?)
    current_time = current_time_seconds()
    if update_time > current_time:
        # If the time is yet to come today, simply subtract the current time from update time
        real_update_time = update_time - current_time
    if update_time < current_time:
        # If the time has passed today, set real_update_time to 24h ahead minus the difference
        real_update_time = (60 * 60 * 24) - abs(current_time - update_time)

    logging.info(f"Update with (name='{update_name}', time={update_time_hhmm}, repeat={repeat}, update-covid={covid}, "
                 f"update-news={news}) scheduled to run in {real_update_time / 60} minutes")

    web_scheduler.enter(real_update_time, 1, run_scheduled_update, (update_name, repeat, covid, news))

    # Add this update to the global updates dictionary
    updates.append({
        "title": update_name,
        "content": f"Time: {update_time_hhmm}, Update news: {news}, Update COVID data: {covid}, Repeat: {repeat}",
    })


def run_scheduled_update(update_name: str, repeat: bool = False, covid: bool = False, news: bool = False) -> None:
    """A wrapper function for actually running the update, necessary so that it can re-add itself to the
    scheduler every time it's run if meant to repeat"""

    logging.info(f"Running scheduled update '{update_name}'")
    if news:
        update_news(update_name)
    if covid:
        update_covid(update_name)
    if repeat:
        # If meant to repeat, every time it runs it adds itself to the scheduler in repeat_interval seconds.
        # Default is 24 hours, configurable in scheduler.
        repeat_interval = get_config_data()["repeat_interval_seconds"]
        repeat_interval = int(repeat_interval)
        web_scheduler.enter(repeat_interval, 1, run_scheduled_update, (update_name, True, covid, news,))
        logging.info(f"Rescheduled repeating update '{update_name}' for {repeat_interval / 60} minutes in the future")
    else:
        # If not repeating, delete itself from the list of updates displayed to the user
        remove_update_from_update_list(update_name)


def remove_update_from_update_list(update_name: str) -> None:
    """Deletes the named update from the 'updates' list (the list shown to the user on the webpage, separate from the
    scheduler queue)."""

    # Go through the list of displayed updates and if any aren't in the list of scheduled events, remove them
    for update in updates:
        if update["title"] == update_name:
            updates.remove(update)
    logging.info(f"Removed update '{update_name}' from list of displayed updates")


def get_event_update_name(event: sched.Event) -> str:
    """Takes a sched.Event object and returns the update_name argument associated with that event. Used to connect
    updates in the update dictionary displayed to user to events in the scheduler queue."""

    # Get the arguments for the event in the scheduler queue, the first argument is the update name
    event_arguments = event.__getattribute__("argument")
    event_update_name = event_arguments[0]

    return event_update_name


def delete_news_article(article_for_deletion_title: str) -> None:
    logging.info(f"Deletion request for article '{article_for_deletion_title}'")
    for article_index, article_dictionary in enumerate(webpage_news_articles):
        if article_dictionary["title"] == article_for_deletion_title:
            deleted_article = webpage_news_articles.pop(article_index)
            deleted_articles.append(article_for_deletion_title)
            logging.info(f"Deleted article with title '{article_for_deletion_title}'")


def delete_update(update_for_deletion_name: str) -> None:
    logging.info(f"Deletion request for update '{update_for_deletion_name}'")

    # For each item in the web scheduler queue, check if its update name matches the update to be deleted
    # If so, cancel the event
    # Doing it by update name instead of event object means repeated updates will also be deleted, as each
    # repetition creates a different event object but they will keep the same name
    for event in web_scheduler.queue:
        if get_event_update_name(event) == update_for_deletion_name:
            web_scheduler.cancel(event)
            remove_update_from_update_list(update_for_deletion_name)
            logging.info(f"Update '{update_for_deletion_name}' has been removed from queue, the new queue is:"
                         f"\n{web_scheduler.queue}\n")


@app.route('/index')
def web_interface() -> str:
    """The main flask application that runs the webpage"""
    web_scheduler.run(blocking=False)

    update_name = request.args.get("two")
    update_time = request.args.get("update")

    # SCHEDULE UPDATE
    # Only triggers if the user has entered both an update name and time
    if update_time and update_name:
        # Get all possible settings for the update
        covid_checkbox = request.args.get("covid-data")
        news_checkbox = request.args.get("news")
        repeat_checkbox = request.args.get("repeat")

        # Check if they have been set or not, and accordingly set variables
        updating_covid = (covid_checkbox == "covid-data")
        updating_news = (news_checkbox == "news")
        repeat = (repeat_checkbox == "repeat")

        # Schedule an update using these variables
        schedule_update(update_time, update_name, covid=updating_covid, news=updating_news, repeat=repeat)

    # DELETE UPDATE
    update_for_deletion_name = request.args.get("update_item")
    if update_for_deletion_name is not None:
        delete_update(update_for_deletion_name)

    # DELETE NEWS ARTICLE
    article_for_deletion = request.args.get("notif")
    if article_for_deletion is not None:
        delete_news_article(article_for_deletion)

    # Get the amount of articles to display from config.json, default is 5 as any more will extend the page length
    article_amount = get_config_data()["number_of_articles_to_display"]
    article_amount = int(article_amount)

    # User may have used inconsistent capitalisation for in the config file so capitalize to ensure UI consistency
    national_location_formatted = webpage_covid_data["nation_location"].capitalize()
    location_formatted = webpage_covid_data["location"].capitalize()

    return render_template("index.html",
                           title="COVID-19 Dashboard",
                           national_7day_infections=webpage_covid_data["national_7day_infections"],
                           local_7day_infections=webpage_covid_data["local_7day_infections"],
                           location=location_formatted,
                           nation_location=national_location_formatted,

                           # These have no label in the HTML so the label is passed in on this end
                           deaths_total=f"Total deaths ({national_location_formatted}): "
                                        + f"{webpage_covid_data['deaths_total']}",

                           hospital_cases=f"Current hospital cases ({national_location_formatted}): "
                                          + f"{webpage_covid_data['hospitalCases']}",

                           # Only display as many news articles as requested in the config file (default 5)
                           news_articles=webpage_news_articles[0:article_amount],

                           updates=updates,
                           image="coronavirus_icon.png",
                           )


# Run the flask webpage itself
if __name__ == '__main__':
    logging.info("\n\nWeb server initialised")
    app.run()
