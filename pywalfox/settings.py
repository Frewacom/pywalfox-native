import os
import json
import logging

from .config import PYWALFOX_CONFIG_DIR, PYWALFOX_CONFIG_PATH


def load_settings():
    """Loads persisted settings from the config file."""
    if not os.path.isfile(PYWALFOX_CONFIG_PATH):
        return {}

    try:
        with open(PYWALFOX_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except (ValueError, IOError) as e:
        logging.warning('Failed to load settings from %s: %s' % (PYWALFOX_CONFIG_PATH, e))
        return {}


def save_settings(settings):
    """Persists settings to the config file, merging with any existing values."""
    current = load_settings()
    current.update(settings)

    try:
        if not os.path.exists(PYWALFOX_CONFIG_DIR):
            os.makedirs(PYWALFOX_CONFIG_DIR)

        with open(PYWALFOX_CONFIG_PATH, 'w') as f:
            json.dump(current, f, indent=2)

        logging.debug('Saved settings to %s' % PYWALFOX_CONFIG_PATH)
    except (IOError, OSError) as e:
        logging.error('Failed to save settings to %s: %s' % (PYWALFOX_CONFIG_PATH, e))


def get_setting(key, default=None):
    """Returns a single setting value, or *default* if not present."""
    return load_settings().get(key, default)
