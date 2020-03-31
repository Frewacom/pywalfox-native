DAEMON_VERSION='2.0'

SOCKET_PATH='/tmp/pywalfox_socket'
PYWAL_COLORS_PATH='~/.cache/wal/colors'
LOG_FILE='daemon.log'

BG_LIGHT_MODIFIER=35

ACTIONS = {
    'VERSION': 'debug:version',
    'OUTPUT': 'debug:output',
    'COLORS': 'action:colors',
    'INVALID_ACTION': 'action:invalid',
    'CSS_ENABLE': 'css:enable',
    'CSS_DISABLE': 'css:disable',
}
