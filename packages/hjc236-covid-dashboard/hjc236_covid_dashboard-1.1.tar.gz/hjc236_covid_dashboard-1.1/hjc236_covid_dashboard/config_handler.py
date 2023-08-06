import json
import os
import sys


def get_config_data() -> dict:
    """Returns the values from the config file as a dictionary"""
    current_location = os.path.abspath(os.path.dirname(__file__))
    path = os.path.abspath(os.path.join(current_location, 'config.json'))

    with open(path, 'r') as config_file:
        data = json.load(config_file)

    return data


class ConfigError(Exception):
    """Exception type for incorrect config file values."""
    pass


def validate_config_data(config_data: dict) -> None:
    """Checks that values in the config file are valid - if not, raise an error. This prevents the program running
    when a user has entered something invalid in the config file."""

    if config_data["news_api_key"] == "":
        raise ConfigError("news_api_key has not been set in config file")

    if config_data["news_language"] not in ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru',
                                            'se', 'ud', 'zh']:
        raise ConfigError(f"{config_data['news_language']} in config file is not a valid option for news_language")

    if int(config_data["number_of_articles_to_display"]) < 0:
        raise ConfigError("number_of_articles_to_display in config file must be at least 0")

    if config_data["local_location_type"] not in ["ltla", "utla", "overview", "nation", "region", "nhsRegion"]:
        raise ConfigError("local_location_type in config file is invalid")

    if config_data["nation_location"] not in ["england", "northern ireland", "scotland", "wales"]:
        raise ConfigError("nation_location in config file is invalid")

    if int(config_data["repeat_interval_seconds"]) <= 0:
        raise ConfigError("repeat_interval_seconds in config file must be greater than 0")
