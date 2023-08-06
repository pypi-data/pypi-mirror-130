"""Базовый класс логгера"""
import logging
import os
import sys

sys.path.append('../')
PATH = os.getcwd()


class ColorFilter(logging.Filter):

    COLOR = {
        "DEBUG": "GREEN",
        "INFO": "GREEN",
        "WARNING": "YELLOW",
        "ERROR": "RED",
        "CRITICAL": "RED",
    }

    def filter(self, record):
        record.color = ColorFilter.COLOR[record.levelname]
        return True


class BaseLogger(object):
    def __init__(self):
        self.logging_level = logging.DEBUG
        self.encoding = 'utf-8'
        self.log_format = logging.Formatter('%(asctime)s %(levelname)s - %(app)s - %(message)s')
        self.stream_handler = logging.StreamHandler(sys.stderr)
        self.path = PATH
        self.logger = None

    def set_stream_handler(self):
        self.stream_handler.setFormatter(self.log_format)
        self.stream_handler.setLevel(logging.ERROR)

    def set_color(self):
        self.logger.addFilter(ColorFilter())

    def critical(self, content):
        self.logger.critical(content)

    def error(self, content):
        self.logger.error(content)

    def debug(self, content):
        self.logger.debug(content)

    def info(self, content):
        self.logger.info(content)





