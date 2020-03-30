import os
import sys
import logging
import argparse

from pywalfox.config import DAEMON_VERSION, LOG_FILE
from pywalfox.daemon import Daemon
from pywalfox.channel.client import Client

parser = argparse.ArgumentParser(description='Pywalfox - Native messaging host')
parser.add_argument('action', nargs='?', default='none', help='sends a message to the addon telling it to update the theme')
parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='runs the daemon in debug mode')
parser.add_argument('-v', '--version', dest='version', action='store_true', help='runs the daemon in debug mode')

def check_python_version(python_version):
    """Checks if the current python version is supported."""
    if python_version < (2,7):
        logging.error('Python version %s is not ssupported' % python_version)
        sys.exit(0)
    else:
        logging.debug('Using python %s.%s' % (python_version[0], python_version[1]))

def send_update_action():
    """Sends the update command to the socket server."""
    client = Client()
    connected = client.start()

    if connected == True:
        client.send_message('update')

def open_log_file():
    """Opens the daemon log file in an editor (default is vi)"""
    log_path = './pywalfox/%s' % LOG_FILE
    if os.environ.get('EDITORs') is not None:
        os.system('$EDITOR %s' % log_path)
    else:
        os.system('vi %s' % log_path)

def print_version():
    """Prints the current version of the daemon."""
    print('v%s' % DAEMON_VERSION)

def handle_exit_args(args):
    """Handles arguments that exit."""
    if args.action == 'update':
        send_update_action()
        sys.exit(1)

    if args.action == 'log':
        open_log_file()
        sys.exit(1)

    if args.version:
        print_version()
        sys.exit(1)

def main():
    """Handles arguments and starts the daemon."""
    python_version = sys.version_info
    check_python_version(python_version)

    args = parser.parse_args()
    handle_exit_args(args)

    daemon = Daemon(python_version.major, args.debug)
    daemon.start()
    daemon.close()

if __name__ == '__main__':
    main()








