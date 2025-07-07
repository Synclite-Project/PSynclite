import os
import configparser
import shutil
from .data import FILE_CONFIG

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def get_value(config, section, key):
    if config.has_section(section):
        if config.has_option(section, key):
            return config.get(section, key)
        else:
            return f"Key '{key}' not found in section '{section}'"
    else:
        return f"Section '{section}' not found"

def check_parameter(config, section, key, value):
    if config.has_section(section):
        if config.has_option(section, key):
            if config.get(section, key) == value:
                return True
            else:
                return False
        else:
            return f"Key '{key}' not found in section '{section}'"
    else:
        return f"Section '{section}' not found"
    
def set_value(file_path, config, section, parametr, value):
    config.set(section, parametr, value)
    with open(file_path, 'w') as f:
        config.write(f)
    
CONFIG = read_config(FILE_CONFIG)


def init():
    """Initialize psynclite by creating the config directory and config file."""

    config_dir = os.path.expanduser('~/.config/psynclite')
    os.path.join(config_dir, 'logs.log')
    
    # check
    if os.path.exists(config_dir):
        #shutil.rmtree(config_dir) # remove
        print("You already have a config directory")
        return 0

    # make a dir
    os.makedirs(config_dir, exist_ok=True)

    config_file = os.path.join(config_dir, 'config.conf')
    
    config = configparser.ConfigParser()

    
    # Add standard configparser entries
    config['GLOBAL'] = {
        'Initialization': 'true'
    }
    config['AI'] = {
        
    }

    # Write the config file
    with open(config_file, 'w') as f:
        config.write(f)