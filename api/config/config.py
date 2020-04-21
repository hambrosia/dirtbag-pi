"""Separate configuration from code and centralize in config.json file"""

from pathlib import Path
import json

import definitions


def get_configs() -> dict:
    """Return configs as dict"""
    root_path = definitions.ROOT_DIR
    config_path = str(root_path) + '/config/config.json'
    config_dict = {}
    with open(config_path) as config_file:
        config_dict = json.load(config_file)
    return config_dict

