import os
import sys
import shutil
import fileinput

from .config import APP_PATH, HOME_PATH, BIN_PATH_UNIX, BIN_PATH_WIN

# We only need these variables when running the setup, so might as well define them here.
MANIFEST_SRC_PATH=os.path.join(APP_PATH, 'assets/manifest.json')
MANIFEST_TARGET_NAME='pywalfox.json'

MANIFEST_TARGET_PATHS_UNIX={
    'FIREFOX': os.path.join('/usr/lib/mozilla/native-messaging-hosts'),
    'CHROME': os.path.join('/etc/opt/chrome/native-messaging-hosts'),
    'CHROMIUM': os.path.join('/etc/chromium/native-messaging-hosts'),
    'BRAVE': os.path.join('/etc/opt/chrome/native-messaging-hosts/'),
    'FIREFOX_USER': os.path.join(HOME_PATH, '.mozilla/native-messaging-hosts'),
    'CHROME_USER': os.path.join(HOME_PATH, 'google-chrome/NativeMessagingHosts'),
    'CHROMIUM_USER': os.path.join(HOME_PATH, 'chromium/NativeMessagingHosts'),
    'BRAVE_USER': os.path.join(HOME_PATH, 'BraveSoftware/Brave-Browser/NativeMessagingHosts/'),
}

MANIFEST_TARGET_PATHS_WIN={
    # TODO: replace these paths with the actual Windows paths
    'FIREFOX': os.path.join('/usr/lib/mozilla/native-messaging-hosts'),
    'CHROME': os.path.join('/etc/opt/chrome/native-messaging-hosts'),
    'CHROMIUM': os.path.join('/etc/chromium/native-messaging-hosts'),
    'BRAVE': os.path.join('/etc/opt/chrome/native-messaging-hosts/'),
    'FIREFOX_USER': os.path.join(HOME_PATH, '.mozilla/native-messaging-hosts'),
    'CHROME_USER': os.path.join(HOME_PATH, 'google-chrome/NativeMessagingHosts'),
    'CHROMIUM_USER': os.path.join(HOME_PATH, 'chromium/NativeMessagingHosts'),
    'BRAVE_USER': os.path.join(HOME_PATH, 'BraveSoftware/Brave-Browser/NativeMessagingHosts/'),
}

def create_hosts_directory(hosts_path):
    """
    Creates the 'native-messaging-hosts' directory if it does not exist.

    :param hosts_path str: the path to create if it does not already exist
    """
    if not os.path.exists(hosts_path):
        os.makedirs(hosts_path)

def remove_existing_manifest(full_path):
    """
    Removes an existing manifest.

    :param full_path str: the path to the manifest
    """
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
    except Exception as e:
        print('Could not remove existing manifest at: %s\n\t%s' % (full_path, str(e)))
        sys.exit(0)

def set_daemon_path(manifest_path, bin_path):
    """
    Replaces the '<path>' placeholder in the default manifest file with the path to the executable.

    :param manifest_path str: the path to the manifest
    :param bin_path str: the path to the daemon executable
    """
    for line in fileinput.FileInput(manifest_path, inplace=1):
        line = line.replace("<path>", bin_path)
        print(line.rstrip('\n'))

def copy_manifest(target_path, bin_path):
    """
    Copies the host manifest to the 'native-messaging-hosts' directory.

    :param target_path str: the path to the hosts directory
    :param bin_path str: the path to the daemon executable
    """
    full_path = os.path.join(target_path, MANIFEST_TARGET_NAME)

    create_hosts_directory(target_path)
    remove_existing_manifest(full_path)

    try:
        shutil.copyfile(MANIFEST_SRC_PATH, full_path)
        print('Copied manifest to: %s' % full_path)
    except Exception as e:
        print('Could not copy manifest to: %s\n\t%s' % (full_path, str(e)))
        sys.exit(0)

    set_daemon_path(full_path, bin_path)

def set_executable_permissions(bin_path):
    """
    Sets the execution permission on the daemon executable.
    https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python

    :param bin_path str: the path to the daemon executable
    """
    try:
        mode = os.stat(bin_path).st_mode
        mode |= (mode & 0o444) >> 2    # copy R bits to X
        os.chmod(bin_path, mode)
    except Exception as e:
        print('Failed to set executable permissions on: %s\n\t%s' % (bin_path, str(e)))
        print('')
        print('Try setting the permissions manually using: chmod +x')
        sys.exit(0)

def get_target_path_key(target_browser, user_only):
    """
    Gets the path to the 'native-messaging-hosts' directory corresponding to
    the targeted browser in the CLI-argument.

    :param target_browser str: the browser to install the manifest to
    :param user_only bool: if the manifest should be installed for the current user only
    :return: the key in MANIFEST_TARGET_PATHS_* corresponding to the manifest path
    :rType: str
    """
    if target_browser == 'firefox':
        if user_only == True:
            return 'FIREFOX_USER'
        else:
            return 'FIREFOX'
    if target_browser == 'chrome':
        if user_only == True:
            return 'CHROME_USER'
        else:
            return 'CHROME'
    if target_browser == 'chromium':
        if user_only == True:
            return 'CHROMIUM_USER'
        else:
            return 'CHROMIUM'
    else:
        print('The browser you selected is currently not (offically) supported by Pywalfox.')
        print('')
        print('If you want it to be added, you can create an issue on GitHub:')
        print('https://github.com/Frewacom/pywalfox-native/issues')
        sys.exit(0)

def win_setup(manifest_path_key):
    """
    Windows specific installation.

    :param manifest_path_key str: the key in MANIFEST_TARGET_PATHS_WIN that corresponds to the target browser
    """
    manifest_path = MANIFEST_TARGET_PATHS_WIN[manifest_path_key]
    copy_manifest(manifest_path, BIN_PATH_WIN)

def unix_setup(manifest_path_key):
    """
    UNIX specific installation.

    :param manifest_path_key str: the key in MANIFEST_TARGET_PATHS_UNIX that corresponds to the target browser
    """
    manifest_path = MANIFEST_TARGET_PATHS_UNIX[manifest_path_key]
    copy_manifest(manifest_path, BIN_PATH_UNIX)
    set_executable_permissions(BIN_PATH_UNIX)

def start_setup(target_browser, user_only):
    """
    Installs the native messaging host manifest.

    :param target_browser str: the name of the browser to install the manifest to
    :param user_only str: if the manifest should be installed for the current user only
    """
    manifest_path_key = get_target_path_key(target_browser, user_only)

    if sys.platform.startswith('win32'):
        win_setup(manifest_path_key)
    else:
        unix_setup(manifest_path_key)

