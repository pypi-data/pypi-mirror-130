"""
Pulls data from the user-set configuration file and ensures that they are valid

Classes:
    ConfigError

Functions:
    get_config_data()
    validate_config_data()
"""

import json
import os

def get_config_data() -> dict:
    """Fetches configuration data from the json file

    Returns:
        A dict mapping configuration file fields to the values they have been set to in the configuration file
    """

    current_location = os.path.abspath(os.path.dirname(__file__))
    path = os.path.abspath(os.path.join(current_location, 'config.json'))

    with open(path, 'r', encoding="utf-8") as config_file:
        data = json.load(config_file)

    return data


class ConfigError(Exception):
    """Exception type for incorrect values in configuration file."""


def validate_config_data(config_data: dict) -> None:
    """Checks that the configuration data is valid.

    Takes a dict of the configuration data and returns a ConfigError if any of the values are invalid

    Args:
        config_data: A dict containing the configuration data

    Raises:
        ConfigError: At least one of the values in the given configuration data was incorrect.
    """

    if config_data["news_api_key"] == "":
        raise ConfigError("news_api_key has not been set in config file. You must configure the program with an API "
                          "key from News API. See the readme for more details.")

    if config_data["news_language"] not in ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru',
                                            'se', 'ud', 'zh']:
        raise ConfigError("Invalid news_language set in config file")

    if int(config_data["number_of_articles_to_display"]) < 0:
        raise ConfigError("number_of_articles_to_display in config file must be at least 0")

    if config_data["local_location_type"] not in ["ltla", "utla", "overview", "nation", "region", "nhsRegion"]:
        raise ConfigError("local_location_type in config file is invalid")

    if config_data["nation_location"] not in ["england", "northern ireland", "scotland", "wales"]:
        raise ConfigError("nation_location in config file is invalid")

    if int(config_data["repeat_interval_seconds"]) <= 0:
        raise ConfigError("repeat_interval_seconds in config file must be greater than 0")
