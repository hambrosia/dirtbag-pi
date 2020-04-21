"""Separate configuration from code and centralize in config.json file"""

import json

def configs() -> dict:
    config_dict = {}
    with open('config.json') as config_file:
        config_dict = json.load(config_file)
    return config_dict

config_dict = configs()

