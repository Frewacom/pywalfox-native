import os
import sys
import shutil
import logging
from config import APP_PATH, HOME_PATH

# We only need these variables when running the setup, so might as well define them here.
MANIFEST_SRC_PATH=os.path.join(APP_PATH, 'assets/manifest.json')
MANIFEST_TARGET_NAME='pywalfox.json'
MANIFEST_TARGET_PATHS_UNIX={
    'FIREFOX': os.path.join('/usr/lib/mozilla/native-messaging-hosts', MANIFEST_TARGET_NAME),
    'CHROME': os.path.join('/etc/opt/chrome/native-messaging-hosts', MANIFEST_TARGET_NAME),
    'FIREFOX_USER': os.path.join(HOME_PATH, '.mozilla/native-messaging-hosts', MANIFEST_TARGET_NAME),
    'CHROME_USER': os.path.join(HOME_PATH, 'google-chrome/NativeMessagingHosts', MANIFEST_TARGET_NAME)
}

def win_setup():
    pass

def unix_setup():
    pass

def start_setup():
    if sys.platform.startswith('win32'):
        win_setup()
    else:
        unix_setup()

