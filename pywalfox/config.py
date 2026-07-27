import os
import sys
import tempfile

DAEMON_VERSION = '2.9.0'

if sys.platform.startswith('win32'):
    UNIX_SOCKET_PATH = None
else:
    UNIX_SOCKET_PATH = os.path.join(tempfile.gettempdir(), 'pywalfox_socket_%d' % os.getuid())
WIN_SOCKET_HOST = ('127.0.0.1', 56744)
WIN_SOCKET_HOST_ALT = ('127.0.0.1', 56745)

HOME_PATH = os.path.expanduser('~')
XDG_CACHE_DIR = os.getenv('XDG_CACHE_HOME', os.path.join(HOME_PATH, '.cache'))
XDG_CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME_PATH, '.config'))
PYWAL_COLORS_PATH = os.path.join(XDG_CACHE_DIR, os.path.join('wal', 'colors.json'))

# This will be set to the executable path by pip
EXECUTABLE_PATH = sys.argv[0]

APP_PATH = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(APP_PATH, 'assets/css')
BIN_PATH_WIN = os.path.join(APP_PATH, 'bin/win.bat')

FIREFOX_PROFILES_PATH_LINUX = os.path.join(HOME_PATH, '.mozilla/firefox')
# Some distro builds put the XDG-compliant profile dir straight under
# $XDG_CONFIG_HOME/firefox; others (confirmed live: Fedora's firefox 153.0)
# nest it under a 'mozilla' vendor subdirectory instead, i.e.
# $XDG_CONFIG_HOME/mozilla/firefox. Check both, vendor-subdir first since
# that's what the profiles.ini fix in issue #8 was actually needed for.
FIREFOX_PROFILES_PATH_LINUX_XDG = os.path.join(XDG_CONFIG_DIR, 'firefox')
FIREFOX_PROFILES_PATH_LINUX_XDG_VENDOR = os.path.join(XDG_CONFIG_DIR, 'mozilla/firefox')
FIREFOX_PROFILES_PATH_WIN = os.path.join(HOME_PATH, 'AppData/Roaming/Mozilla/Firefox')
FIREFOX_PROFILES_PATH_DARWIN = os.path.join(HOME_PATH, 'Library/Application Support/Firefox')

# Thunderbird's profile layout mirrors Firefox's exactly (same toolkit), including
# both possible XDG-compliant paths above.
THUNDERBIRD_PROFILES_PATH_LINUX = os.path.join(HOME_PATH, '.thunderbird')
THUNDERBIRD_PROFILES_PATH_LINUX_XDG = os.path.join(XDG_CONFIG_DIR, 'thunderbird')
THUNDERBIRD_PROFILES_PATH_LINUX_XDG_VENDOR = os.path.join(XDG_CONFIG_DIR, 'mozilla/thunderbird')
THUNDERBIRD_PROFILES_PATH_WIN = os.path.join(HOME_PATH, 'AppData/Roaming/Thunderbird')
THUNDERBIRD_PROFILES_PATH_DARWIN = os.path.join(HOME_PATH, 'Library/Application Support/Thunderbird')

# Apps supported as separate native-messaging-host callers. Each gets its own persisted
# settings (see settings.py's per-app helpers) so that installing/fixing one never
# overwrites the other's profile_path -- see custom_css.detect_calling_app().
APP_FIREFOX = 'firefox'
APP_THUNDERBIRD = 'thunderbird'
SUPPORTED_APPS = (APP_FIREFOX, APP_THUNDERBIRD)
DEFAULT_APP = APP_FIREFOX

LOG_FILE_COUNT = 1
LOG_FILE_MAX_SIZE = 1000*200 # 0.2 mb
LOG_FILE_DATE_FORMAT = '%m-%d-%Y %I:%M:%S'
LOG_FILE_FORMAT = '[%(asctime)s] %(levelname)s:%(message)s'
LOG_FILE_PATH = os.path.join(XDG_CACHE_DIR, 'pywalfox.log')

if sys.platform.startswith('win32'):
    PYWALFOX_CONFIG_DIR = os.path.join(os.getenv('APPDATA', os.path.join(HOME_PATH, 'AppData', 'Roaming')), 'pywalfox')
elif sys.platform.startswith('darwin'):
    PYWALFOX_CONFIG_DIR = os.path.join(HOME_PATH, 'Library', 'Application Support', 'pywalfox')
else:
    PYWALFOX_CONFIG_DIR = os.path.join(XDG_CONFIG_DIR, 'pywalfox')

PYWALFOX_CONFIG_PATH = os.path.join(PYWALFOX_CONFIG_DIR, 'config.json')

ACTIONS = {
    'VERSION': 'debug:version',
    'OUTPUT': 'debug:output',
    'COLORS': 'action:colors',
    'INVALID_ACTION': 'action:invalid',
    'CSS_ENABLE': 'css:enable',
    'CSS_DISABLE': 'css:disable',
    'CSS_FONT_SIZE': 'css:font:size',
    'THEME_MODE': 'theme:mode',
}

COMMANDS = {
    'THEME_MODE_DARK': 'theme:mode:dark',
    'THEME_MODE_LIGHT': 'theme:mode:light',
    'THEME_MODE_AUTO': 'theme:mode:auto',
    'UPDATE': 'action:update',
}
