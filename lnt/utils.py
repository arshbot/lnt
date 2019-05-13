import os
import lnt.constants as const

def ensure_default_config_exists():
    """ Checks if default config file exists and creates if not for fallback """
    exists = os.path.exists(const.DEFAULT_DIR_PATH)
    if not exists:
        create_config_folder()
        create_conf()

    return

def check_config_exists(fld=const.DEFAULT_DIR_PATH):
    """ Check if config file exists """
    return

def create_config_folder(fld=const.DEFAULT_DIR_PATH):
    """ Creates a config folder at the specified location """
    return

def create_conf(f=const.DEFAULT_CONF_PATH):
    return
