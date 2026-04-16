import os
import sys
import atexit
import logging
import argparse
import subprocess

from .daemon import Daemon
from .utils.logger import setup_logging
from .config import DAEMON_VERSION, LOG_FILE_PATH, COMMANDS, EXECUTABLE_PATH
from .settings import save_settings

if sys.platform.startswith('win32'):
    from .channel.win.client import Client
else:
    from .channel.unix.client import Client

# This is an ugly fix that is needed to be able to execute
# pywalfox from Firefox without using a separate shell script.
#
# Firefox passes in a few arguments to the executable which are not valid
# arguments for the executable. To circumvent this, we need to ignore the
# errors and simply start the executable anyway.
#
# https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging#exchanging_messages
def handle_error(self, message=None):
    if len(sys.argv) == 3 and sys.argv[2] == 'pywalfox@frewacom.org':
        apply_saved_profile_path()
        setup_logging(False, False)
        run_daemon()
    else:
        parser.print_help()
        sys.exit(1)

parser = argparse.ArgumentParser(description='Pywalfox native messaging host v%s' % DAEMON_VERSION)

# Register custom error handler
parser.error = handle_error

setup_group = parser.add_argument_group('install/uninstall')
start_group = parser.add_argument_group('start')
parser.add_argument('action',
        nargs='?',
        default=None,
        metavar='ACTION',
        help='available actions are install, uninstall, start, update, log, dark, light and auto')
parser.add_argument('-v', '--version',
        dest='version',
        action='store_true',
        help='displays current version of daemon')
start_group.add_argument('-p', '--print',
        dest='print_mode',
        action='store_true',
        help='writes debugging output from native messaging host to stdout')
start_group.add_argument('--verbose',
        dest='verbose',
        action='store_true',
        help='runs native messaging host in verbose mode')
setup_group.add_argument('-g', '--global',
        dest='global_install',
        action='store_true',
        help='installs/uninstalls native host manifest globally')
setup_group.add_argument('--executable',
        dest='custom_path',
        nargs='?',
        type=str,
        help='use a custom path for the `pywalfox` executable')
setup_group.add_argument('--manifest-path',
        dest='manifest_path',
        type=str,
        default=None,
        help='overrides native messaging host manifest directory path')
setup_group.add_argument('--profile-path',
        dest='profile_path',
        type=str,
        default=None,
        help='overrides profiles directory path')

def apply_saved_profile_path(cli_override=None):
    """
    Applies the Firefox profile path override.
    Uses the CLI flag if provided, otherwise falls back to the persisted setting.
    """
    path = cli_override
    if path is None:
        from pywalfox.settings import get_setting
        path = get_setting('profile_path')

    if path is not None:
        from pywalfox.custom_css import set_profile_path_override
        set_profile_path_override(path)

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

def send_client_command(message):
    """
    Sends a message to the socket server.

    :param message str: the message to send
    """
    client = Client()

    for host in client.hosts:
        connected = client.connect(host)
        if connected is True:
            client.send_message(message)

def send_update_action():
    """Sends an update command to the addon, triggering a refetch of colors"""
    send_client_command(COMMANDS['UPDATE'])

def send_theme_mode_dark():
    save_settings({'theme_mode': 'dark'})
    print('Saved theme mode: dark')
    send_client_command(COMMANDS['THEME_MODE_DARK'])

def send_theme_mode_light():
    save_settings({'theme_mode': 'light'})
    print('Saved theme mode: light')
    send_client_command(COMMANDS['THEME_MODE_LIGHT'])

def send_theme_mode_auto():
    save_settings({'theme_mode': 'auto'})
    print('Saved theme mode: auto')
    send_client_command(COMMANDS['THEME_MODE_AUTO'])

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

def no_executable():
    print('Could not find executable path, please re-run the installation with:')
    print('pywalfox install --executable <path-to-pywalfox-executable>')
    sys.exit(1)

def handle_args(args):
    """Handles CLI arguments."""
    if args.version:
        print_version()
        sys.exit(0)

    if args.action == 'update':
        send_update_action()
        sys.exit(0)

    if args.action == 'dark':
        send_theme_mode_dark()
        sys.exit(0)

    if args.action == 'light':
        send_theme_mode_light()
        sys.exit(0)

    if args.action == 'auto':
        send_theme_mode_auto()
        sys.exit(0)

    if args.action == 'log':
        open_log_file()
        sys.exit(0)

    if args.action == 'start':
        apply_saved_profile_path(args.profile_path)
        setup_logging(args.verbose, args.print_mode)
        run_daemon()

    if args.action == 'install':
        from pywalfox.install import start_setup

        path_to_use = EXECUTABLE_PATH
        if args.custom_path:
            path_to_use = args.custom_path
        else:
            # Try to find a valid path
            if not os.path.isabs(path_to_use):
                path_to_use = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    os.path.basename(__file__)
                )
            if not os.path.isabs(path_to_use) or "__main__.py" in path_to_use:
                no_executable()

        if not os.path.exists(path_to_use) or not os.path.isfile(path_to_use):
            no_executable()

        start_setup(args.global_install, path_to_use,
                     manifest_path=args.manifest_path)

        if args.profile_path:
            from pywalfox.settings import save_settings
            save_settings({'profile_path': args.profile_path})
            print('Saved custom Firefox profile path: %s' % args.profile_path)
        else:
            print('')
            print('NOTE: Firefox forks (e.g. Librewolf) may require custom paths, e.g.')
            print('  pywalfox install --manifest-path ~/.mozilla/native-messaging-hosts \\')
            print('                   --profile-path  ~/.config/librewolf/librewolf')

        sys.exit(0)

    if args.action == 'uninstall':
        from pywalfox.install import start_uninstall
        start_uninstall(args.global_install,
                        manifest_path=args.manifest_path)
        sys.exit(0)

    parser.print_help()

def main():
    """Application entry point."""
    args = parser.parse_args()
    handle_args(args)

if __name__ == '__main__':
    main()
