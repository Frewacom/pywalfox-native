DAEMON_VERSION='2.0'

UNIX_SOCKET_PATH='/tmp/pywalfox_socket'
WIN_SOCKET_HOST = ('127.0.0.1', 56744)

PYWAL_COLORS_PATH='~/.cache/wal/colors'

LOG_FILE='daemon.log'
LOG_FILE_COUNT=1
LOG_FILE_MAX_SIZE=1000*200 # 0.2 mb

BG_LIGHT_MODIFIER=35

ACTIONS = {
    'VERSION': 'debug:version',
    'OUTPUT': 'debug:output',
    'COLORS': 'action:colors',
    'INVALID_ACTION': 'action:invalid',
    'CSS_ENABLE': 'css:enable',
    'CSS_DISABLE': 'css:disable',
}
