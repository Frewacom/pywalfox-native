import os

DAEMON_VERSION='2.2'

UNIX_SOCKET_PATH='/tmp/pywalfox_socket'
WIN_SOCKET_HOST = ('127.0.0.1', 56744)

SUPPORTED_BROWSERS=['firefox']

HOME_PATH=os.path.expanduser('~')
XDG_CACHE_DIR = os.getenv('XDG_CACHE_HOME', os.path.join(HOME_PATH, '.cache'))
PYWAL_COLORS_PATH=os.path.join(XDG_CACHE_DIR, 'wal/colors')

APP_PATH=os.path.dirname(os.path.abspath(__file__))
BIN_PATH_UNIX=os.path.join(APP_PATH, 'bin/main.sh')
BIN_PATH_WIN=os.path.join(APP_PATH, 'bin/win.bat')
CSS_PATH=os.path.join(APP_PATH, 'assets/css')

FIREFOX_PATH_LINUX=os.path.join(HOME_PATH, '.mozilla/firefox/*.default-release')
FIREFOX_PATH_DARWIN=os.path.join(HOME_PATH, 'Library/Application\ Support/Firefox/Profiles/*.default-release*')
FIREFOX_PATH_WIN=os.path.join(HOME_PATH, 'AppData/Roaming/Mozilla/Firefox/Profiles/*.default-*')

LOG_FILE_PATH=os.path.join(APP_PATH, 'daemon.log')
LOG_FILE_COUNT=1
LOG_FILE_MAX_SIZE=1000*200 # 0.2 mb
LOG_FILE_FORMAT='[%(asctime)s] %(levelname)s:%(message)s'
LOG_FILE_DATE_FORMAT='%m-%d-%Y %I:%M:%S'

ACTIONS={
    'VERSION': 'debug:version',
    'OUTPUT': 'debug:output',
    'COLORS': 'action:colors',
    'INVALID_ACTION': 'action:invalid',
    'CSS_ENABLE': 'css:enable',
    'CSS_DISABLE': 'css:disable',
    'CSS_FONT_SIZE': 'css:font:size',
}

