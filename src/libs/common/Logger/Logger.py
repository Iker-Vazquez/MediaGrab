#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Logger.py
"""
Description: Logger class for logging messages to a specified log file.
Author: Iker Vazquez
Email: iker-vazquez@users.noreply.github.com
Date: 2023-10-29
"""

import logging
import os
import json

from enum import Enum


class LoggerLevel(Enum):
    """Enumeración para los niveles de logging."""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Logger:
    """Logger class for handling log messages."""

    # region Global params
    debug_level: int = LoggerLevel.DEBUG.value
    log_file_path: str = 'logFile.log'
    # endregion Global params

    def __init__(self, log_file: str = './logFile.log', config_json: str = './config.json') -> None:
        """
        Initializes the Logger instance.

        *Arguments*:
        - log_file --> str : Path to the log file.
        - configJson --> str : Path to the configuration JSON file.

        *Returns*:
        - None

        *Examples*:
        - logger = Logger('/path/to/logFile.log')
        - logger = Logger()
        - logger = Logger('/path/to/log_file.log', '/path/to/config.json')

        *Notes*:
        - Creates the log directory if it does not exist.
        """
        self.load_configuration(config_json)

        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format=(
                '%(asctime)s - [%(filename)s][%(name)s:%(funcName)s] - '
                '%(levelname)s \t- %(message)s'
            ),
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self._logger = logging.getLogger()

    def load_configuration(self, config_path: str) -> None:
        """
        Loads the configuration from a JSON file.

        *Arguments*:
        - config_path --> str : Path to the configuration JSON file.

        *Returns*:
        - None

        *Examples*:
        - load_configuration('/path/to/config.json')

        *Notes*:
        - This method reads the configuration file and sets the debug level and log file path.
        """
        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                debug_config = config.get("debugConfig", {})
                Logger.debug_level = debug_config.get("debugLevel", LoggerLevel.DEBUG.value)
                Logger.log_file_path = debug_config.get("logFilePath", './logs/logFile.log')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al leer {config_path}: {e}")
            Logger.debug_level = LoggerLevel.DEBUG.value
            Logger.log_file_path = './logs/logFile.log'

    def write_debug(self, message: str) -> None:
        """
        Logs a debug message.
        Only if debugLevel on config.json is less or equal to DEBUG level.

        *Arguments*:
        - message --> str : The debug message to log.

        *Returns*:
        - None

        *Examples*:
        - logger.write_debug("Debug message")

        *Notes*:
        - This method logs at DEBUG level.
        """
        if Logger.debug_level <= LoggerLevel.DEBUG.value:
            self._logger.debug(message, stacklevel=2)

    def write_info(self, message: str) -> None:
        """
        Logs an info message.
        Only if debugLevel on config.json is less or equal to INFO level.

        *Arguments*:
        - message --> str : The info message to log.

        *Returns*:
        - None

        *Examples*:
        - logger.write_info("Info message")

        *Notes*:
        - No notes.
        """

        if Logger.debug_level <= LoggerLevel.INFO.value:
            self._logger.info(message, stacklevel=2)

    def write_warning(self, message: str) -> None:
        """
        Logs a warning message.
        Only if debugLevel on config.json is less or equal to WARNING level.

        *Arguments*:
        - message --> str : The warning message to log.

        *Returns*:
        - None

        *Examples*:
        - logger.write_warning("Warning message")

        *Notes*:
        - No notes.
        """
        if Logger.debug_level <= LoggerLevel.WARNING.value:
            self._logger.warning(message, stacklevel=2)

    def write_error(self, message: str) -> None:
        """
        Logs an error message.
        Only if debugLevel on config.json is less or equal to ERROR level.

        *Arguments*:
        - message --> str : The error message to log.

        *Returns*:
        - None

        *Examples*:
        - logger.write_error("Error message")

        *Notes*:
        - No notes.
        """
        if Logger.debug_level <= LoggerLevel.ERROR.value:
            self._logger.error(message, stacklevel=2)

    def write_critical(self, message: str) -> None:
        """
        Logs a critical message.
        Only if debugLevel on config.json is less or equal to CRITICAL level.

        *Arguments*:
        - message --> str : The critical message to log.

        *Returns*:
        - None

        *Examples*:
        - logger.write_critical("Critical message")

        *Notes*:
        - No notes.
        """
        if Logger.debug_level <= LoggerLevel.CRITICAL.value:
            self._logger.critical(message, stacklevel=2)

    @classmethod
    def get_debug_level(cls) -> int:
        """Gets the current debug level for logging.

        *Arguments*:
        - None

        *Returns*:
        - debug level (int): The current logging level set in Logger.

        *Examples*:
        - Logger.get_debug_level()

        *Notes*:
        - This method retrieves the class-wide debug level without needing an instance.
        """
        return cls.debug_level
