"""Separate configuration from code and centralize in config.json file"""

import json

import definitions


ROOT_PATH = definitions.ROOT_DIR

def get_configs() -> dict:
    """Return configs as dict"""
    config_path = str(ROOT_PATH) + '/config/config.json'
    config_dict = {}
    with open(config_path) as config_file:
        config_dict = json.load(config_file)
    return config_dict

def get_secrets() -> dict:
    """Return secrets as dict"""
    secrets_path = str(ROOT_PATH) + '/config/secret.json'
    secrets_dict = {}
    with open(secrets_path) as secrets_file:
        secrets_dict = json.load(secrets_file)
    return secrets_dict

