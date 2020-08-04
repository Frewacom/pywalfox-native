import os
import sys
import atexit
import logging
import argparse
import subprocess

from .daemon import Daemon
from .utils.logger import setup_logging
from .config import DAEMON_VERSION, LOG_FILE_PATH

if sys.platform.startswith('win32'):
    from .channel.win.client import Client
else:
    from .channel.unix.client import Client

parser = argparse.ArgumentParser(description='Pywalfox - Native messaging host')
setup_group = parser.add_argument_group('install/uninstall')
start_group = parser.add_argument_group('start')
parser.add_argument('action',
        nargs='?',
        default=None,
        metavar='ACTION',
        help='available actions are install, start, update, log and uninstall')
parser.add_argument('-v', '--version',
        dest='version',
        action='store_true',
        help='displays the current version of the daemon')
start_group.add_argument('-p', '--print',
        dest='print_mode',
        action='store_true',
        help='writes debugging output from the native messaging host to stdout')
start_group.add_argument('--verbose',
        dest='verbose',
        action='store_true',
        help='runs the native messaging host in verbose mode')
setup_group.add_argument('-g', '--global',
        dest='global_install',
        action='store_true',
        help='installs/uninstalls the native host manifest globally')

def get_python_version():
    """Gets the current python version and checks if it is supported."""
    python_version = sys.version_info
    version_label = '%s.%s.%s' % (python_version[0], python_version[1], python_version[2])
    if python_version < (2, 7):
        logging.error('Python version %s is not supported' % version_label)
        sys.exit(1)
    else:
        logging.debug('Using python %s' % version_label)

    return python_version

def send_update_action():
    """Sends the update command to the socket server."""
    client = Client()

    for host in client.hosts:
        connected = client.connect(host)
        if connected is True:
            client.send_message('update')

def open_log_file():
    """Opens the daemon log file in an editor."""
    if os.path.isfile(LOG_FILE_PATH):
        if not sys.platform.startswith('win32'):
            editor = os.getenv('EDITOR', 'vi')
        else:
            editor = 'nano' # fallback

        subprocess.call([editor, LOG_FILE_PATH])
    else:
        print('No log file exists')

def print_version():
    """Prints the current version of the daemon."""
    print('v%s' % DAEMON_VERSION)

def run_daemon():
    """Starts the daemon."""
    daemon = Daemon(get_python_version().major)
    atexit.register(daemon.close)
    daemon.start()

def handle_args(args):
    """Handles CLI arguments."""
    if args.version:
        print_version()
        sys.exit(0)

    if args.action == 'update':
        send_update_action()
        sys.exit(0)

    if args.action == 'start':
        setup_logging(args.verbose, args.print_mode)
        run_daemon()

    if args.action == 'log':
        open_log_file()
        sys.exit(0)

    if args.action == 'install':
        from pywalfox.install import start_setup
        start_setup(args.global_install)
        sys.exit(0)

    if args.action == 'uninstall':
        from pywalfox.install import start_uninstall
        start_uninstall(args.global_install)
        sys.exit(0)

    # If no action was specified
    parser.print_help()

def main():
    """Application entry point."""
    args = parser.parse_args()
    handle_args(args)

if __name__ == '__main__':
    main()
