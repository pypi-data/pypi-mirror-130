import logging
import sched
import time
import os

from uk_covid19 import Cov19API

from hjc236_covid_dashboard.config_handler import get_config_data

log_file_location = get_config_data()["log_file_path"]
current_location = os.path.abspath(os.path.dirname(__file__))
path = os.path.abspath(os.path.join(current_location, log_file_location))
logging.basicConfig(filename=path, level=logging.DEBUG, format="%(asctime)s %(message)s")


def parse_csv_data(csv_filename: str) -> list[str]:
    """Returns a list of strings for the rows in a given CSV file.

    NOTE: This is a purely demonstrative function made to fit the specification, actual data handling is done with JSON
    """
    current_location = os.path.abspath(os.path.dirname( __file__ ))
    file_path = os.path.abspath(os.path.join(current_location, csv_filename))

    with open(file_path, 'r') as csv_file:
        csv_rows = csv_file.read().splitlines()

    return csv_rows


def process_covid_csv_data(covid_csv_data: list[str]) -> tuple[int, int, int]:
    """Returns the number of cases over the last 7 days, current number of hospital cases, and cumulative deaths from
    given COVID data

    NOTE: This is a purely demonstrative function made to fit the specification, actual data handling is done with
    covid_data_handler.process_covid_JSON_data()
    """

    # Split CSV rows to create a 2D array.
    for i in range(0, len(covid_csv_data)):
        covid_csv_data[i] = covid_csv_data[i].split(",")

    last7days_cases = 0
    for i in range(3, 10):
        last7days_cases += int(covid_csv_data[i][6])

    current_hospital_cases = int(covid_csv_data[1][5])
    total_deaths = int(covid_csv_data[14][4])

    return last7days_cases, current_hospital_cases, total_deaths


def make_API_call(filters: list[str], structure: dict) -> dict:
    """Returns a JSON object containing COVID data based on the given filters and structure"""
    data = Cov19API(filters=filters, structure=structure)
    result = data.get_json()

    return result


def convert_JSON_data(list_of_dictionaries: list[dict]) -> dict[dict]:
    """Converts the list of dictionaries returned from the API to a single dictionary, where an item's key is the
    date of the COVID data, and the value is a dictionary of the remaining metrics"""

    dictionary_of_dictionaries = {}
    for i in range(0, len(list_of_dictionaries)):
        old_dictionary = list_of_dictionaries[i]
        date = old_dictionary.pop("date")
        dictionary_of_dictionaries[date] = old_dictionary

    return dictionary_of_dictionaries


def process_covid_json_data(local_json: dict, national_json: dict) -> dict:
    """Returns a dictionary of specified metrics based on the JSON files of local and national COVID data"""

    deaths_total = None
    hospitalCases = None
    national_7day_infections = 0
    local_7day_infections = 0

    counter = 0
    skipped_first_day = False
    for date in national_json.keys():
        current_data = national_json[date]

        # For cumDeaths and hospitalCases, find the first non-empty cells and use these values
        if current_data["cumDeaths"] is not None and deaths_total is None:
            deaths_total = current_data["cumDeaths"]

        if current_data["hospitalCases"] is not None and hospitalCases is None:
            hospitalCases = current_data["hospitalCases"]

        # Add up all the non-empty rows of 'newCases' until we have 7 (ie a week's worth of data)
        if current_data["newCases"] is not None and counter < 7:
            # Skip first day of COVID data as it is incomplete
            if skipped_first_day:
                national_7day_infections += current_data["newCases"]
                counter += 1
            else:
                skipped_first_day = True

    counter = 0
    skipped_first_day = False
    for date in local_json.keys():
        current_data = local_json[date]

        if current_data["newCases"] is not None and counter < 7:
            if skipped_first_day:
                local_7day_infections += current_data["newCases"]
                counter += 1
            else:
                skipped_first_day = True

    covid_data = {
        "local_7day_infections": local_7day_infections,  # local case total in the last 7 days

        "national_7day_infections": national_7day_infections,  # national case total in the last 7 days
        "hospitalCases": hospitalCases,  # current amount of hospitalised cases
        "deaths_total": deaths_total,  # current amount of cumulative deaths
    }

    return covid_data


def covid_API_request(location: str = "exeter", location_type: str = "ltla") -> dict:
    """Returns a dictionary of up-to-date COVID data via Public Health England's API"""

    nation_location = get_config_data()["nation_location"]

    national_filters = ["areaType=nation", f"areaName={nation_location}"]
    local_filters = [f"areaType={location_type}", f"areaName={location}"]

    local_structure = {"date": "date", "areaType": "areaType", "areaName": "areaName",
                       "newCases": "newCasesBySpecimenDate"}

    national_structure = {"date": "date", "areaType": "areaType", "areaName": "areaName",
                          "newCases": "newCasesByPublishDate", "hospitalCases": "hospitalCases",
                          "cumDeaths": "cumDailyNsoDeathsByDeathDate"}

    local_data = make_API_call(local_filters, local_structure)
    national_data = make_API_call(national_filters, national_structure)

    # strip headers from JSON data and convert from lists of dictionaries to one dictionary where key = date and
    # value = dictionary of remaining data
    local_data = convert_JSON_data(local_data["data"])
    national_data = convert_JSON_data(national_data["data"])

    processed_covid_data = process_covid_json_data(local_data, national_data)

    # Append location details to the dictionary here so the website can use them
    processed_covid_data["location"] = location
    processed_covid_data["nation_location"] = nation_location

    return processed_covid_data


def schedule_covid_updates(update_interval: int, update_name: str) -> None:
    """Updates COVID data every update_interval seconds in an update called update_name

    NOTE: This is a purely demonstrative function made to fit the specification, all updates are scheduled by the
    function web_interface.schedule_update()"""

    scheduler = sched.scheduler(time.time, time.sleep)

    # Wrapper function that can re-add itself to the scheduler each time it's run to ensure it repeats
    def scheduled_data_update() -> None:
        # Get local location and type from config file
        location = get_config_data()["local_location"]
        location_type = get_config_data()["local_location_type"]

        # Writes to a global variable for COVID data so it's updated whenever the scheduled API request happens
        global covid_data
        covid_data = covid_API_request(location, location_type)
        # Adds itself to the scheduler again when called so that it loops every update_interval seconds
        scheduler.enter(update_interval, 1, scheduled_data_update)

    # Add the event to the scheduler for the first time; after this it will keep adding itself again when called
    scheduler.enter(update_interval, 1, scheduled_data_update)
    scheduler.run(blocking=False)


def update_covid(update_name: str) -> None:
    """Updates the global webpage_covid_data list, this is in main.py and is what gets passed to the
    web page"""

    global webpage_covid_data
    location = get_config_data()["local_location"]
    location_type = get_config_data()["local_location_type"]

    webpage_covid_data = covid_API_request(location, location_type)


