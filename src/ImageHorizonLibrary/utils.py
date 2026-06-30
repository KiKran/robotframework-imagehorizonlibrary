# -*- coding: utf-8 -*-
from platform import platform, architecture
from subprocess import call
from robot.api import logger as LOGGER


PLATFORM = platform()
ARCHITECTURE = architecture()


def is_windows():
    return PLATFORM.lower().startswith('windows')


def is_mac():
    return PLATFORM.lower().startswith('darwin')


def is_linux():
    return PLATFORM.lower().startswith('linux')


def is_java():
    return PLATFORM.lower().startswith('java')


def has_retina():
    if is_mac():
        # Will return 0 if there is a retina display
        return call("system_profiler SPDisplaysDataType | grep 'Retina'", shell=True) == 0
    return False


def check_timeout(timeout):
    try:
        value = float(timeout)
    except (TypeError, ValueError) as e:
        raise ValueError(
            f'timeout "{timeout}" (type {type(timeout)}) is not convertible to float') from e
    if value == 0.0:
        LOGGER.warn('Timeout is set to 0; timeout-aware keywords such as '
                    'Wait For will not wait at all. Is this intended?')
    return value


def has_cv():
    has_cv = True
    try:
        import cv2
    except ModuleNotFoundError as err:
        has_cv = False
    return has_cv
