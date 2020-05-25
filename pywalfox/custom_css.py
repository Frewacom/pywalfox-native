from __future__ import print_function

import os
import sys
import shutil
import logging
import fileinput
from .config import CSS_PATH, FIREFOX_PROFILES_PATH_WIN, FIREFOX_PROFILES_PATH_DARWIN, FIREFOX_PROFILES_PATH_LINUX

try:
    import configparser
except ImportError: # python 2.7.x
    import ConfigParser as configparser


def get_firefox_profiles_path():
    """Gets the correct Firefox profiles folder based on the current OS."""
    if sys.platform.startswith('win32'):
        return FIREFOX_PROFILES_PATH_WIN
    elif sys.platform.startswith('darwin'):
        return FIREFOX_PROFILES_PATH_DARWIN
    else:
        return FIREFOX_PROFILES_PATH_LINUX

def get_profile_section(profile):
    """Finds the section that stores the name of the default profile."""
    for section in profile.sections():
        if 'Install' in section:
            return section

def get_profile_from_ini():
    """
    Reads the default profile name for the current Firefox installation
    from profiles.ini and returns the absolute path to the profile.

    :return: path to the current profile folder
    :rType: str
    """
    firefox_profiles_path = get_firefox_profiles_path()
    ini_path = os.path.join(firefox_profiles_path, 'profiles.ini')
    if not os.path.exists(ini_path):
        logging.error('Could not find profiles.ini in Firefox profiles folder')
        return False

    profile = configparser.ConfigParser()
    profile.read(ini_path)

    profile_section = get_profile_section(profile)
    profile_path = os.path.normpath(os.path.join(firefox_profiles_path, profile.get(profile_section, 'Default')))
    if not os.path.exists(profile_path):
        logging.error('The profile path retrieved from profiles.ini does not exist: %s' % profile_path)
        return False

    return profile_path

def get_firefox_chrome_path():
    """
    Retrieves the path to the 'chrome' folder in the default Firefox profile

    :return: the absolute path to the chrome folder
    :rType: str
    """
    profile_path = get_profile_from_ini()

    if not profile_path:
        logging.error('Could not find Firefox profile folder')
        return False

    chrome_path = os.path.join(profile_path, 'chrome')
    if not os.path.exists(chrome_path):
        logging.debug('Creating non-existant chrome directory')
        os.makedirs(chrome_path)

    logging.debug('Found chrome directory at path: %s' % chrome_path)
    return chrome_path

def enable_custom_css(chrome_path, name):
    """
    Applies a CSS file but putting it in the 'chrome' directory.

    :param chrome_path str: the path to the chrome directory
    :param name str: the name of the css file to apply
    :return: (success, message)
    :rType: tuple
    """
    filename = add_css_file_extension(name)
    logging.debug('Enabling custom CSS file: %s' % filename)
    try:
        shutil.copy(os.path.join(CSS_PATH, filename), os.path.join(chrome_path, filename))
        logging.debug('%s was enabled' % filename)
        return (True, 'Custom CSS: %s has been enabled' % filename)
    except Exception as e:
        logging.error('%s could not be enabled: %s' % (filename, str(e)))
        return (False, 'Could not copy custom CSS to folder: %s' % str(e))

def disable_custom_css(chrome_path, name):
    """
    Disabled a CSS file but removing it from the 'chrome' directory.

    :param chrome_path str: the path to the chrome directory
    :param name str: the name of the css file to disable
    :return: (success, message)
    :rType: tuple
    """
    filename = add_css_file_extension(name)
    logging.debug('Disabling custom CSS file: %s' % filename)
    try:
        os.remove(os.path.join(chrome_path, filename))
        logging.debug('%s was disabled' % filename)
        return (True, 'Custom CSS: %s has been disabled' % filename)
    except Exception as e:
        logging.error('%s could not be disabled: %s' % (filename, str(e)))
        return (False, 'Could not remove custom CSS: %s' % str(e))

def set_font_size(chrome_path, name, size):
    """
    Sets the default font size in a CSS file.

    :param chrome_path str: the path to the chrome directory
    :param name str: the name of the css file to disable
    :param size int: the new font size
    :return: (success, message)
    :rType: tuple
    """
    filename = add_css_file_extension(name)
    logging.debug('Setting font size to %s in custom CSS file: %s' % (size, filename))
    try:
        for line in fileinput.input(os.path.join(chrome_path, filename), inplace=True):
            if '--pywalfox-font-size:' in line:
                print('  --pywalfox-font-size: %spx;' % size)
            else:
                print(line, end='')
        return (True, 'Font size was set to: %s' % size)
    except Exception as e:
        error_msg = 'Could not set font size: %s' % str(e)
        logging.error(error_msg)
        return (False, error_msg)

def add_css_file_extension(name):
    """
    Appends the CSS file extension to a string.

    :return: name with '.css' append at the end append at the end
    :rType: string
    """
    return '%s.css' % name
