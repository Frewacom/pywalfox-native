import os
import sys
import shutil
import logging
import fileinput
from .config import (
    CSS_PATH,
    FIREFOX_PROFILES_PATH_WIN,
    FIREFOX_PROFILES_PATH_DARWIN,
    FIREFOX_PROFILES_PATH_LINUX,
    FIREFOX_PROFILES_PATH_LINUX_XDG,
    FIREFOX_PROFILES_PATH_LINUX_XDG_VENDOR,
    THUNDERBIRD_PROFILES_PATH_WIN,
    THUNDERBIRD_PROFILES_PATH_DARWIN,
    THUNDERBIRD_PROFILES_PATH_LINUX,
    THUNDERBIRD_PROFILES_PATH_LINUX_XDG,
    THUNDERBIRD_PROFILES_PATH_LINUX_XDG_VENDOR,
    APP_FIREFOX,
    APP_THUNDERBIRD,
    SUPPORTED_APPS,
    DEFAULT_APP,
)

try:
    import configparser
except ImportError: # python 2.7.x
    import ConfigParser as configparser


# Maps each supported app to its OS-specific default profile directory
# candidates, in the same (legacy, xdg) shape used for Firefox previously,
# plus a vendor-subdirectory XDG variant (see FIREFOX_PROFILES_PATH_LINUX_XDG_VENDOR).
_PROFILE_PATH_DEFAULTS = {
    APP_FIREFOX: {
        'win32': FIREFOX_PROFILES_PATH_WIN,
        'darwin': FIREFOX_PROFILES_PATH_DARWIN,
        'linux_legacy': FIREFOX_PROFILES_PATH_LINUX,
        'linux_xdg': FIREFOX_PROFILES_PATH_LINUX_XDG,
        'linux_xdg_vendor': FIREFOX_PROFILES_PATH_LINUX_XDG_VENDOR,
    },
    APP_THUNDERBIRD: {
        'win32': THUNDERBIRD_PROFILES_PATH_WIN,
        'darwin': THUNDERBIRD_PROFILES_PATH_DARWIN,
        'linux_legacy': THUNDERBIRD_PROFILES_PATH_LINUX,
        'linux_xdg': THUNDERBIRD_PROFILES_PATH_LINUX_XDG,
        'linux_xdg_vendor': THUNDERBIRD_PROFILES_PATH_LINUX_XDG_VENDOR,
    },
}

# Per-app profile path overrides, set via set_profile_path_override(). Kept
# separate per app so that e.g. installing/fixing Firefox's path can never
# clobber an already-working Thunderbird override, and vice versa.
_profile_path_overrides = {}


def set_profile_path_override(path, app=DEFAULT_APP):
    """Sets a custom profile path for *app*, overriding OS-specific defaults."""
    _profile_path_overrides[app] = path


def detect_calling_app():
    """
    Best-effort detection of which app (Firefox or Thunderbird) spawned this
    process via native messaging. Native messaging manifests only support a
    fixed `path` field with no way to pass custom arguments or environment
    variables to distinguish callers, so this is resolved by inspecting the
    parent process instead.

    Only implemented for Linux (via /proc), where this whole setup was
    developed and tested. Falls back to DEFAULT_APP everywhere else and on
    any failure -- this matches pywalfox's existing pre-multi-app behavior
    exactly, so nothing regresses for callers this can't identify.

    :return: one of SUPPORTED_APPS
    :rType: str
    """
    if not sys.platform.startswith('linux'):
        return DEFAULT_APP

    try:
        ppid = os.getppid()
        with open('/proc/%d/comm' % ppid, 'r') as f:
            parent_name = f.read().strip().lower()
    except (IOError, OSError):
        return DEFAULT_APP

    for app in SUPPORTED_APPS:
        if app in parent_name:
            return app

    return DEFAULT_APP


def get_profiles_path(app):
    """Gets the correct profiles folder for *app*, based on the current OS."""
    if app not in _PROFILE_PATH_DEFAULTS:
        app = DEFAULT_APP

    override = _profile_path_overrides.get(app)
    if override is not None:
        return override

    defaults = _PROFILE_PATH_DEFAULTS[app]

    if sys.platform.startswith('win32'):
        return defaults['win32']
    elif sys.platform.startswith('darwin'):
        return defaults['darwin']
    else:
        # Newer Firefox/Thunderbird versions may use XDG_CONFIG_HOME, either
        # directly ($XDG_CONFIG_HOME/firefox) or nested under a 'mozilla'
        # vendor subdirectory ($XDG_CONFIG_HOME/mozilla/firefox) depending on
        # the distro/build -- check the vendor-subdir variant first since
        # that's the one that was previously undetectable entirely (#8).
        if os.path.isfile(os.path.join(defaults['linux_xdg_vendor'], 'profiles.ini')):
            return defaults['linux_xdg_vendor']
        if os.path.isfile(os.path.join(defaults['linux_xdg'], 'profiles.ini')):
            return defaults['linux_xdg']
        return defaults['linux_legacy']


def get_firefox_profiles_path():
    """Retained for backwards compatibility -- use get_profiles_path(app) instead."""
    return get_profiles_path(APP_FIREFOX)


def _resolve_default_profile(profile_config):
    """
    Resolves the actual active default profile from a parsed profiles.ini,
    matching how Firefox/Thunderbird themselves pick it: an [InstallXXXX]
    section's locked Default= entry takes priority over a bare [ProfileN]
    Default=1 flag when both are present (this is what real installs with a
    profile group / multiple profiles actually use -- ProfileN's own
    ordering is not guaranteed to reflect which one is actually active).

    Falls back to the first [ProfileN] section with Default=1, then to
    Profile0, for older/simpler profiles.ini layouts that predate the
    Install-section convention.

    :param profile_config ConfigParser: a parsed profiles.ini
    :return: (section_name, path_value, is_relative) or None if unresolvable
    :rType: tuple or None
    """
    install_sections = [s for s in profile_config.sections() if s.startswith('Install')]
    for section in install_sections:
        if not profile_config.has_option(section, 'Default'):
            continue
        default_path = profile_config.get(section, 'Default')
        # The Install section's Default= value is itself a relative profile
        # path (e.g. "abcd1234.default-release"), not a [ProfileN] section
        # name -- find the [ProfileN] section describing it to get IsRelative.
        for section_name in profile_config.sections():
            if not section_name.startswith('Profile'):
                continue
            if profile_config.get(section_name, 'Path', fallback=None) == default_path:
                return (
                    section_name,
                    profile_config.get(section_name, 'Path'),
                    profile_config.get(section_name, 'IsRelative', fallback='1'),
                )
        # No matching [ProfileN] section (unusual, but the Default= value
        # itself is still a usable relative path in every real-world layout).
        return (None, default_path, '1')

    for section_name in profile_config.sections():
        if not section_name.startswith('Profile'):
            continue
        if profile_config.get(section_name, 'Default', fallback='0') == '1':
            return (
                section_name,
                profile_config.get(section_name, 'Path'),
                profile_config.get(section_name, 'IsRelative', fallback='1'),
            )

    if profile_config.has_section('Profile0'):
        return (
            'Profile0',
            profile_config.get('Profile0', 'Path'),
            profile_config.get('Profile0', 'IsRelative', fallback='1'),
        )

    return None


def get_profile_from_ini(app=DEFAULT_APP):
    """
    Reads the active default profile for *app* from profiles.ini and returns
    the absolute path to the profile.

    :param app str: which app's profiles.ini to read, e.g. 'firefox'
    :return: path to the current profile folder
    :rType: str
    """
    profiles_path = get_profiles_path(app)
    ini_path = os.path.join(profiles_path, 'profiles.ini')
    if not os.path.exists(ini_path):
        logging.error('Could not find profiles.ini in %s profiles folder' % app)
        return False

    profile_config = configparser.ConfigParser()
    profile_config.read(ini_path)

    resolved = _resolve_default_profile(profile_config)
    if resolved is None:
        logging.error('Could not resolve a default profile from profiles.ini for %s' % app)
        return False

    _section_name, path_value, relative_value = resolved

    if relative_value == '1':
        profile_path = os.path.normpath(os.path.join(profiles_path, path_value))
        logging.debug('%s profile path is relative' % app)
    else:
        profile_path = os.path.normpath(path_value)
        logging.debug('%s profile path is absolute' % app)

    if not os.path.exists(profile_path):
        logging.error('The profile path retrieved from profiles.ini does not exist: %s' % profile_path)
        return False

    return profile_path

def get_chrome_path(app=DEFAULT_APP):
    """
    Retrieves the path to the 'chrome' folder in the active default profile
    for *app*.

    :param app str: which app's chrome folder to resolve, e.g. 'firefox'
    :return: the absolute path to the chrome folder
    :rType: str
    """
    profile_path = get_profile_from_ini(app)

    if not profile_path:
        return False

    chrome_path = os.path.join(profile_path, 'chrome')
    if not os.path.exists(chrome_path):
        logging.debug('Creating non-existant chrome directory')
        os.makedirs(chrome_path)

    logging.debug('Found chrome directory at path: %s' % chrome_path)
    return chrome_path


def get_firefox_chrome_path():
    """Retained for backwards compatibility -- use get_chrome_path(app) instead."""
    return get_chrome_path(APP_FIREFOX)

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
        if os.path.isfile(os.path.join(chrome_path, filename)):
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
