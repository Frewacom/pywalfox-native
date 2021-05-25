import os

DAEMON_VERSION = '2.7.2'

UNIX_SOCKET_PATH = '/tmp/pywalfox_socket'
UNIX_SOCKET_PATH_ALT = '/tmp/pywalfox_socket_alt'
WIN_SOCKET_HOST = ('127.0.0.1', 56744)
WIN_SOCKET_HOST_ALT = ('127.0.0.1', 56745)

SUPPORTED_BROWSERS = ['firefox']

HOME_PATH = os.path.expanduser('~')
XDG_CACHE_DIR = os.getenv('XDG_CACHE_HOME', os.path.join(HOME_PATH, '.cache'))
PYWAL_COLORS_PATH = os.path.join(XDG_CACHE_DIR, os.path.join('wal', 'colors.json'))

APP_PATH = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(APP_PATH, 'assets/css')
BIN_PATH_WIN = os.path.join(APP_PATH, 'bin/win.bat')
BIN_PATH_UNIX = os.path.join(APP_PATH, 'bin/main.sh')

FIREFOX_PROFILES_PATH_LINUX = os.path.join(HOME_PATH, '.mozilla/firefox')
FIREFOX_PROFILES_PATH_WIN = os.path.join(HOME_PATH, 'AppData/Roaming/Mozilla/Firefox')
FIREFOX_PROFILES_PATH_DARWIN = os.path.join(HOME_PATH, 'Library/Application Support/Firefox')

LOG_FILE_COUNT = 1
LOG_FILE_MAX_SIZE = 1000*200 # 0.2 mb
LOG_FILE_DATE_FORMAT = '%m-%d-%Y %I:%M:%S'
LOG_FILE_FORMAT = '[%(asctime)s] %(levelname)s:%(message)s'
LOG_FILE_PATH = os.path.join(XDG_CACHE_DIR, 'pywalfox.log')

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
