"""
Manages the retrieval, processing, and formatting of news articles via the News API

Functions:
    news_API_request()
    update_news()
    format_news_data()
"""

import logging
import requests
from flask import Markup
from hjc236_covid_dashboard.config_handler import get_config_data, validate_config_data


log_file_location = get_config_data()["log_file_path"]
logging.basicConfig(filename=log_file_location, level=logging.DEBUG, format="%(asctime)s %(message)s")


def news_API_request(covid_terms: str = "Covid COVID-19 coronavirus") -> list[dict]:
    config_data = get_config_data()
    validate_config_data(config_data)
    """Returns relevant current news articles from the News API based on the covid_terms argument"""
    api_key = config_data["news_api_key"]
    endpoint = "https://newsapi.org/v2/everything?"
    lang = get_config_data()["news_language"]
    formatted_url = endpoint + f"q={covid_terms}" + f"&apiKey={api_key}" + "&sortBy=publishedAt" + f"&language={lang}"
    response = requests.get(formatted_url, timeout=10)
    news_data = response.json()

    if news_data["status"] == "error":
        # News articles are not returned from API...
        if news_data["code"] == "apiKeyInvalid":
            # Because the API key was invalid
            logging.error("Invalid News API key in configuration file")
        else:
            # For some other reason
            logging.error("Failed to get articles from News API")

        # Still return the response, in this case it will consist of an error message
        return news_data

    else:
        # News articles are correctly returned from API, get rid of headers and keep 'articles'
        news_data = news_data["articles"]
    return news_data


def update_news(update_name: str, deleted_articles: list[dict] = None) -> None:
    """Updates the global webpage_news_articles list with new content from the News API"""
    logging.info(f"Updating news due to update '{update_name}'")

    covid_terms = get_config_data()["news_covid_terms"]
    news_data = news_API_request(covid_terms)

    # If a list of deleted articles has been passed, check all new articles and delete them if their titles match
    # This is to ensure deleted articles do not return on page refresh
    if deleted_articles is not None:
        for article_index, article_dictionary in enumerate(news_data):
            if article_dictionary["title"] in deleted_articles:
                news_data.pop(article_index)

    # webpage_news_articles is the global list of articles in main.py passed to the webpage
    global webpage_news_articles
    webpage_news_articles = format_news_data(news_data)


def format_news_data(news_articles: list[dict]) -> list[dict]:
    """Changes the given list of news article dictionaries and alters them to look more user-friendly on the webpage.

    For each article: Replaces 'content' values with 'description' values if they exist for the article,
    which are better for displaying a concise article description. Formats titles to become HTML hyperlinked to the
    article's URL with flask.Markup()
    """

    formatted_articles = news_articles

    for article in formatted_articles:
        # 'description' is formatted in a more user-friendly way so it is better to display this to the user,
        # but not all articles have it - if they don't, better to just show the content than nothing
        if article["description"] is not None:
            article["content"] = article["description"]

        # Add hyperlink leading to the article's URL to all titles
        url = article["url"]
        title = article["title"]
        formatted_title = f"<a href={url}>{title}</a>"
        article["title"] = Markup(formatted_title)

    return formatted_articles
