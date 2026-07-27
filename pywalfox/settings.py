import os
import json
import logging

from .config import PYWALFOX_CONFIG_DIR, PYWALFOX_CONFIG_PATH, DEFAULT_APP


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


def get_app_setting(app, key, default=None):
    """
    Returns a setting value scoped to a specific calling app (e.g. 'firefox',
    'thunderbird'), so Firefox and Thunderbird don't share values like
    profile_path that must differ between them.

    Falls back to the legacy top-level (unscoped) value for the same key if no
    per-app value has been saved yet -- this keeps existing single-browser
    installs working unchanged after upgrading, instead of silently losing a
    profile_path that was set before per-app settings existed.

    :param app str: the app the setting is scoped to, e.g. 'firefox'
    :param key str: the setting name
    :param default: returned if neither a per-app nor a legacy value exists
    """
    settings = load_settings()
    apps = settings.get('apps', {})
    app_settings = apps.get(app, {})

    if key in app_settings:
        return app_settings[key]

    # Legacy fallback: settings saved before per-app scoping existed.
    return settings.get(key, default)


def save_app_setting(app, key, value):
    """
    Persists a setting value scoped to a specific calling app, merging with
    any existing per-app values. Does not touch the legacy top-level key with
    the same name, if one exists, so an older pywalfox version reading the
    same config file (e.g. after a downgrade) still sees its expected shape.

    :param app str: the app the setting is scoped to, e.g. 'firefox'
    :param key str: the setting name
    :param value: the value to persist
    """
    settings = load_settings()
    apps = settings.setdefault('apps', {})
    app_settings = apps.setdefault(app, {})
    app_settings[key] = value
    save_settings(settings)


def get_profile_path(app=DEFAULT_APP):
    """Returns the persisted profile_path override for *app*, if any."""
    return get_app_setting(app, 'profile_path')


def save_profile_path(app, path):
    """Persists a profile_path override scoped to *app*."""
    save_app_setting(app, 'profile_path', path)
