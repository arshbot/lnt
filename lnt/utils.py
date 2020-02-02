import os
import lnt.constants as const
import click

# Mark config utils
def check_config_exists(fld=const.DEFAULT_DIR_PATH):
    """ Check if config file exists """
    exists = os.path.exists(const.DEFAULT_CONF_PATH)
    return exists

def check_lnt_folder_exists(fld=const.DEFAULT_DIR_PATH):
    """ Checks if the lnt folder specified exists """
    exists = os.path.exists(fld)
    return exists

def create_lnt_folder(fld=const.DEFAULT_DIR_PATH):
    """ Creates a config folder and nested dirs at the specified location """
    os.mkdir(fld)
    return

def create_config(config_path=const.DEFAULT_CONF_PATH):
    """ Creates an empty config file. Assumes default lnt dir exists """
    with open(config_path, "w") as config:
        config.write(const.EMPTY_CONF)
    return

def validate_config(config):
    passed = True

    if not 'MacaroonPath' in config['LND']:
        passed = False
        raise click.ClickException("Required parameter 'MacaroonPath' not found in conf")
    elif not 'TlsCert' in config['LND']:
        passed = False
        raise click.ClickException("Required parameter 'TlcCert' not found in conf")
    elif not 'Host' in config['LND']:
        passed = False
        raise click.ClickException("Required parameter 'Host' not found in conf")

    if 'testnet' in config['LNT']:

        try:
            config['LNT'].getboolean('testnet')
        except ValueError:
            click.ClickException("testnet has to bool")

    if not passed:
       raise click.ClickException("Provided config file failed validation")

    return config, passed

# Mark cache utils
def check_cache_exists(fld=const.DEFAULT_CACHE_DIR_PATH):
    """ Check if cache files exist"""
    exists = os.path.exists(const.DEFAULT_CACHE_DIR_PATH)
    if exists:
        if not os.path.exists(const.DEFAULT_CACHE_NODE_PATH):
            return False
        return True
    else:
        return False

def create_cache_dir(fld=const.DEFAULT_CACHE_DIR_PATH):
    try:
        os.mkdir(fld)
    except FileExistsError:
        return

def create_node_cache(cache_path=const.DEFAULT_CACHE_NODE_PATH):
    with open(cache_path, "w") as config:
        config.write(const.EMPTY_NODE_CACHE)
    return
