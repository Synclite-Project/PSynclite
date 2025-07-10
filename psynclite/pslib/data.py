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

# path to file config
FILE_CONFIG = os.path.expanduser('~/.config/psynclite/config.conf')
# path to notification history file
NOTIFICATION_HISTORY_FILE = os.path.expanduser('~/.config/psynclite/notifications.json')
# notification categories
NOTIFICATION_CATEGORIES = ['System', 'Sound', 'Brightness', 'Media', 'Battery', 'Network', 'Backup', 'Info']
# path to config directory
CONFIG_DIR = os.path.expanduser('~/.config/psynclite')
# path to log file
LOG_FILE = os.path.expanduser('~/.config/psynclite/logs.log')
        
