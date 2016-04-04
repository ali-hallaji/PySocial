# PySocial Import
from core import cursor


def get_settings(settings_type, key):
    settings = cursor.settings.find_one({'settings_type': settings_type})

    if settings:

        if key:
            return settings.get(key, None)

        else:
            return settings

    else:
        raise Exception('Get Settings: No settings in DB')


def general_settings(key=None):
    return get_settings('GeneralSettings', key)


def default_status(key=None):
    return get_settings('DefaultStatus', key)
