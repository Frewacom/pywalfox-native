#!/usr/bin/env python

import os
import sys
import logging
import argparse

from config import DAEMON_VERSION
from daemon import Daemon
from channel.client import Client
from utils.logger import *

parser = argparse.ArgumentParser(description='Pywalfox - Native messaging host')
parser.add_argument('action', nargs='?', default='none', help='sends a message to the addon telling it to update the theme')
parser.add_argument('--verbose', dest='verbose', action='store_true', help='runs the daemon in verbose mode with debugging output')
parser.add_argument('-p', '--print', dest='print_mode', action='store_true', help='prints the debugging output instead of writing to logfile')
parser.add_argument('-v', '--version', dest='version', action='store_true', help='displays the current version of the daemon')

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

def check_python_version(python_version):
    """Checks if the current python version is supported."""
    version_label = '%s.%s.%s' % (python_version[0], python_version[1], python_version[2])
    if python_version < (2,7):
        logging.error('Python version %s is not supported' % version_label)
        sys.exit(0)
    else:
        logging.debug('Using python %s' % version_label)

def send_update_action():
    """Sends the update command to the socket server."""
    client = Client()
    connected = client.start()

    if connected == True:
        client.send_message('update')

def open_log_file():
    """Opens the daemon log file in an editor (default is vi)"""
    if os.path.isfile(LOG_FILE):
        if os.environ.get('EDITORs') is not None:
            os.system('$EDITOR %s' % LOG_FILE)
        else:
            os.system('vi %s' % LOG_FILE)
    else:
        print('No log file exists')

def print_version():
    """Prints the current version of the daemon."""
    print('v%s' % DAEMON_VERSION)

def main():
    """Handles arguments and starts the daemon."""
    args = parser.parse_args()
    handle_exit_args(args)

    setup_logging(args.verbose, args.print_mode)

    python_version = sys.version_info
    check_python_version(python_version)

    daemon = Daemon(python_version.major)
    daemon.start()
    daemon.close()

if __name__ == '__main__':
    main()








