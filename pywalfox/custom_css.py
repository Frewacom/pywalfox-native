import os
import glob
import logging

def get_firefox_chrome_path():
    """
    Retrieves the path to the 'chrome' folder in the default Firefox profile

    :return: the absolute path to the chrome folder
    :rType: str
    """
    profile_path = glob.glob('%s/*.default-release' % os.path.expanduser('~/.mozilla/firefox'))

    if len(profile_path) < 1:
        return False

    chrome_path = os.path.join(profile_path[0], 'chrome')
    if not os.path.exists(chrome_path):
        os.makedirs(chrome_path)

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
    try:
        shutil.copy('./assets/%s' % filename, '%s/%s' % (chrome_path, filename))
        return (True, 'Custom CSS: "%s" has been enabled' % filename)
    except Exception as e:
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
    try:
        os.remove('%s/%s' % (chrome_path, filename))
        return (True, 'Custom CSS: "%s" has been disabled' % filename)
    except Exception as e:
        return (False, 'Could not remove custom CSS: %s' % str(e))

def add_css_file_extension(name):
    """
    Appends the CSS file extension to a string.

    :return: name with '.css' append at the end append at the end
    :rType: string
    """
    return '%s.css' % name
