import os
import sys
import shutil
import fileinput

from .config import APP_PATH, HOME_PATH, BIN_PATH_UNIX, BIN_PATH_WIN

if sys.platform.startswith('win32'):
    try:
        import _winreg as winreg
    except ImportError:
        import winreg

# We only need these variables when running the setup, so might as well define them here.
MANIFEST_SRC_PATH = os.path.join(APP_PATH, 'assets/manifest.json')
MANIFEST_TARGET_NAME = 'pywalfox.json'

WIN_REGISTRY_PATH = r'Software\Mozilla\NativeMessagingHosts\pywalfox'
MANIFEST_TARGET_PATH_WIN = os.path.join(HOME_PATH, '.pywalfox')

MANIFEST_TARGET_PATHS_LINUX = {
    'FIREFOX': os.path.join('/usr/lib/mozilla/native-messaging-hosts'),
    'FIREFOX_USER': os.path.join(HOME_PATH, '.mozilla/native-messaging-hosts'),
}

MANIFEST_TARGET_PATHS_DARWIN = {
    'FIREFOX': os.path.join('/Library/Application Support/Mozilla/NativeMessagingHosts'),
    'FIREFOX_USER': os.path.join(HOME_PATH, 'Library/Application Support/Mozilla/NativeMessagingHosts'),
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
        sys.exit(1)

def normalize_path(target_path):
    """
    Replaces backslashes with forward slashes.

    :param target_path str: the path to normalize
    :return: the normalized path
    :rType: str
    """
    return (r'%s' % target_path).replace('\\', '/')

def get_full_manifest_path(target_path):
    return os.path.join(target_path, MANIFEST_TARGET_NAME)

def set_daemon_path(manifest_path, bin_path):
    """
    Replaces the '<path>' placeholder in the default manifest file with the path to the executable.

    :param manifest_path str: the path to the manifest
    :param bin_path str: the path to the daemon executable
    """
    normalized_path = normalize_path(bin_path)
    for line in fileinput.FileInput(manifest_path, inplace=1):
        line = line.replace("<path>", normalized_path)
        print(line.rstrip('\n'))

    print('Set daemon executable path to: %s' % normalized_path)

def copy_manifest(target_path, bin_path):
    """
    Copies the host manifest to the 'native-messaging-hosts' directory.

    :param target_path str: the path to the hosts directory
    :param bin_path str: the path to the daemon executable
    """
    full_path = get_full_manifest_path(target_path)
    create_hosts_directory(target_path)
    remove_existing_manifest(full_path)

    try:
        shutil.copyfile(MANIFEST_SRC_PATH, full_path)
        print('Copied manifest to: %s' % full_path)
    except Exception as e:
        print('Could not copy manifest to: %s\n\t%s' % (full_path, str(e)))
        sys.exit(1)

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
        print('Set execute permissions on daemon executable')
    except Exception as e:
        print('Failed to set executable permissions on: %s\n\t%s' % (bin_path, str(e)))
        print('')
        print('Try setting the permissions manually using: chmod +x')
        sys.exit(1)

def get_target_path_key(user_only):
    """
    Gets the path key for the 'native-messaging-hosts' directory based on
    if the manifest should be installed locally or globally.

    :param user_only bool: if the manifest should be installed for the current user only
    :return: the key in MANIFEST_TARGET_PATHS_* corresponding to the manifest path
    :rType: str
    """
    if user_only is True:
        return 'FIREFOX_USER'
    else:
        return 'FIREFOX'

def setup_register(manifest_path_key):
    """
    Imports the winreg module and returns the hkey based on if the
    manifest should be installed for the current user only, or for all users.
    """
    hkey = winreg.HKEY_CURRENT_USER
    if manifest_path_key == 'FIREFOX':
        hkey = winreg.HKEY_LOCAL_MACHINE

    return hkey

def delete_registry_keys(manifest_path_key):
    """Tries to delete an existing registry key holding the path to the manifest."""
    hkey = setup_register(manifest_path_key)

    try:
        reg_key = winreg.OpenKey(hkey, WIN_REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
        print('Found existing registry key and opened with write permissions')
    except Exception:
        print('No existing registry key found')
        return

    try:
        winreg.DeleteValue(reg_key, '')
        winreg.DeleteKey(hkey, WIN_REGISTRY_PATH)
        print('Deleted registry key: %s' % WIN_REGISTRY_PATH)
    except Exception as e:
        print('Failed to remove existing registry key: %s' % str(e))
        return

def win_setup(manifest_path_key):
    """Windows installation."""
    hkey = setup_register(manifest_path_key)

    try:
        reg_key = winreg.OpenKey(hkey, WIN_REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
        print('Opened registry key with write permissions')
    except Exception:
        reg_key = winreg.CreateKey(hkey, WIN_REGISTRY_PATH)
        print('Created new registry key')

    try:
        normalized_target_path = normalize_path(os.path.join(MANIFEST_TARGET_PATH_WIN, MANIFEST_TARGET_NAME))
        winreg.SetValue(reg_key, '', winreg.REG_SZ, normalized_target_path)
        print('Set value of registry: %s to %s' % (WIN_REGISTRY_PATH, normalized_target_path))
    except Exception as e:
        print('Failed to set registry key: %s\n%s' % (reg_key, str(e)))
        sys.exit(1)

    copy_manifest(MANIFEST_TARGET_PATH_WIN, BIN_PATH_WIN)

def linux_setup(manifest_path_key):
    """Linux installation."""
    manifest_path = MANIFEST_TARGET_PATHS_LINUX[manifest_path_key]
    copy_manifest(manifest_path, BIN_PATH_UNIX)
    set_executable_permissions(BIN_PATH_UNIX)

def darwin_setup(manifest_path_key):
    """MacOS installation."""
    manifest_path = MANIFEST_TARGET_PATHS_DARWIN[manifest_path_key]
    copy_manifest(manifest_path, BIN_PATH_UNIX)
    set_executable_permissions(BIN_PATH_UNIX)

def start_setup(user_only):
    """
    Installs the native messaging host manifest.

    :param user_only bool: if the manifest should be installed for the current user only
    """
    manifest_path_key = get_target_path_key(user_only)

    if sys.platform.startswith('win32'):
        win_setup(manifest_path_key)
    elif sys.platform.startswith('darwin'):
        darwin_setup(manifest_path_key)
    else:
        linux_setup(manifest_path_key)

def start_uninstall(user_only):
    """
    Tries to remove an existing manifest and delete registry keys (win32).

    :param user_only bool: if the manifest should be uninstalled for the current user only
    """
    manifest_path_key = get_target_path_key(user_only)

    if sys.platform.startswith('win32'):
        manifest_path = MANIFEST_TARGET_PATH_WIN
        delete_registry_keys(manifest_path_key)
    elif sys.platform.startswith('darwin'):
        manifest_path = MANIFEST_TARGET_PATHS_DARWIN[manifest_path_key]
    else:
        manifest_path = MANIFEST_TARGET_PATHS_LINUX[manifest_path_key]

    full_manifest_path = get_full_manifest_path(manifest_path)
    remove_existing_manifest(full_manifest_path)
