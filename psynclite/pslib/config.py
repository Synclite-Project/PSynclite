import os
import configparser

COLORS = {
    'reset': '\033[0m',
    'red': '\033[31m',
    'yellow': '\033[33m',
    'green': '\033[32m',
    'blue': '\033[34m',
    'cyan': '\033[36m',
    'bold': '\033[1m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'gray': '\033[90m'
}

NOTIFICATION_HISTORY_FILE = os.path.expanduser('~/.config/psynclite/notifications.json')
NOTIFICATION_CATEGORIES = ['System', 'Sound', 'Brightness', 'Media', 'Battery', 'Network', 'Backup', 'Info']
AI_CONFIG_FILE = os.path.expanduser('~/.config/psynclite/ai_model.conf')
CONFIG_DIR = os.path.expanduser('~/.config/psynclite')
LOG_FILE = os.path.expanduser('~/.config/psynclite/logs.log')
API_KEY_FILE = os.path.expanduser('~/.config/psynclite/api_key.txt')

def init():
    """Initialize psynclite by creating the config directory and config file."""
    import shutil
    import configparser

    config_dir = os.path.expanduser('~/.config/psynclite')

    # Проверка существует ли директория
    if os.path.exists(config_dir):
        # Удалть её, если да
        shutil.rmtree(config_dir)

    # Create the directory
    os.makedirs(config_dir, exist_ok=True)

    # Create the config file
    config_file = os.path.join(config_dir, 'config.conf')
    os.path.join(config_dir, 'logs.log')
    config = configparser.ConfigParser()

    
    # Add standard configparser entries
    config['AI'] = {
        'model': 'Value1',
        'apikey': 'Value2',
    }

    # Write the config file
    with open(config_file, 'w') as f:
        config.write(f)