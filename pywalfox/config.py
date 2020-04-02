import os

DAEMON_VERSION='2.0'

UNIX_SOCKET_PATH='/tmp/pywalfox_socket'
WIN_SOCKET_HOST = ('127.0.0.1', 56744)

HOME_PATH=os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~'))
PYWAL_COLORS_PATH=os.path.join(HOME_PATH, '.cache/wal/colors')

APP_PATH=os.path.dirname(os.path.abspath(__file__))
CSS_PATH=os.path.join(APP_PATH, 'assets/css')

LOG_FILE_PATH=os.path.join(APP_PATH, 'daemon.log')
LOG_FILE_COUNT=1
LOG_FILE_MAX_SIZE=1000*200 # 0.2 mb
LOG_FILE_FORMAT='[%(asctime)s] %(levelname)s:%(message)s'
LOG_FILE_DATE_FORMAT='%m-%d-%Y %I:%M:%S'

BG_LIGHT_MODIFIER=35

ACTIONS={
    'VERSION': 'debug:version',
    'OUTPUT': 'debug:output',
    'COLORS': 'action:colors',
    'INVALID_ACTION': 'action:invalid',
    'CSS_ENABLE': 'css:enable',
    'CSS_DISABLE': 'css:disable',
}

