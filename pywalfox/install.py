import os
import sys
import shutil
import logging
from config import APP_PATH

def win_setup():
    pass

def unix_setup():
    print(os.getcwd())

def start_setup():
    if sys.platform.startswith('win32'):
        win_setup()
    else:
        unix_setup()

