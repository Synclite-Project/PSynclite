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
