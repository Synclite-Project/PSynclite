import os

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

# Base configuration directory
CONFIG_DIR = os.path.expanduser('~/.config/psynclite')
os.makedirs(CONFIG_DIR, exist_ok=True)

# Individual file paths (fully backward-compatible)
FILE_CONFIG = os.path.join(CONFIG_DIR, 'config.conf')
NOTIFICATION_HISTORY_FILE = os.path.join(CONFIG_DIR, 'notifications.json')
LOG_FILE = os.path.join(CONFIG_DIR, 'logs.log')

# Notification categories
NOTIFICATION_CATEGORIES = [
    'System', 'Sound', 'Brightness', 'Media', 'Battery',
    'Network', 'Backup', 'Info'
]