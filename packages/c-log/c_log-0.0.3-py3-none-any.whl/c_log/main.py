#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Additional utilities
"""

from time import time
from datetime import datetime
from .config import Config


def ts() -> str:
    """
    Get the current date and time in the format% YYYY-MM-DD HH:MM:SS
    """
    get_time = time()
    data = datetime.fromtimestamp(get_time).strftime('%Y-%m-%d %H:%M:%S')
    return data


class Message(object):
    """
    Formation of a log.
    Usage example:

    from c_log import msg

    msg.ok('Test message')
    msg.ok('Test message', 'core')

    msg.info('Test message')
    msg.info('Test message', 'core')

    msg.warn('Test message')
    msg.warn('Test message', 'core')

    msg.error('Test message')
    msg.error('Test message', 'core')
    """
    def __init__(self, log_level=None, color=None, end_color=Config.ENDCOLOR):
        """
        Initialization
        """
        self.log_level = log_level
        self.color = color
        self.end_color = end_color

    def __print_msg(self, message=str, module_name=None) -> None:
        if module_name is None:
            return print(
                self.color,
                ts(),
                self.log_level,
                message,
                self.end_color
            )
        else:
            module_name = f'[{module_name.upper()}]'
            return print(
                self.color,
                ts(),
                self.log_level,
                module_name,
                message,
                self.end_color
            )

    def info(self, message=str, module_name=None) -> None:
        """
        Returning a message of type INFO
        """
        self.log_level = '[INFO]'
        self.color = Config.BLUE
        self.__print_msg(message, module_name)

    def ok(self, message=str, module_name=None) -> None:
        """
        Returning a message of type OK
        """
        self.log_level = '[OK]'
        self.color = Config.GREEN
        self.__print_msg(message, module_name)

    def warn(self, message=str, module_name=None) -> None:
        """
        Returning a message of type WARN
        """
        self.log_level = '[WARN]'
        self.color = Config.YELLOW
        self.__print_msg(message, module_name)

    def error(self, message=str, module_name=None) -> None:
        """
        Returning a message of type ERROR
        """
        self.log_level = '[ERROR]'
        self.color = Config.RED
        self.__print_msg(message, module_name)


msg = Message()
