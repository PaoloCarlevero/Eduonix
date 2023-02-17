"""This module provides the To-Do config functionality."""
# cli_to_do/config.py

import configparser
from pathlib import Path # Allow cross-platform way to handle system paths

import typer

from cli_to_do import (DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__)) # Return the path to a directory where we can store configuration
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini" # Path to the configuration file

def _init_config_file() -> int:
    """ Create configuration file """
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return DIR_ERROR
    return SUCCESS

def _create_database(db_path: str) -> int:
    """ Create to-do database""" 
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSerror:
        return DB_WRITE_ERROR
    return SUCCESS

def init_app(db_path: str) -> int:
    """Initialize the application's configuartion file and database"""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code
    return SUCCESS

