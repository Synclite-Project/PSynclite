import os
import configparser
import shutil
from .data import FILE_CONFIG

def read_config(file_path):
    """Read configuration safely"""
    config = configparser.ConfigParser()
    if not os.path.exists(file_path):
        return config  
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
    
def set_value(file_path, config, section, key, value) -> None:
    """Set or update a value in config and write to file"""
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        config.write(f)


def init():
    """Initialize psynclite configuration directory and file"""
    try:
        config_dir = os.path.expanduser('~/.config/psynclite')
        config_file = os.path.join(config_dir, 'config.conf')

        # если файл существует — уточнить у пользователя
        if os.path.exists(config_file):
            print("⚙️  Файл конфигурации уже существует.")
            choice = input("Пересоздать конфигурацию? (y/N): ").strip().lower()
            if choice != 'y':
                print("⏹  Инициализация отменена.")
                return 0
            else:
                print("🧹  Старый конфиг будет перезаписан.\n")

        os.makedirs(config_dir, exist_ok=True)

        print("Добро пожаловать в установщик PSynclite!")
        print("Эта утилита создаст базовую конфигурацию.\n")

        apikey = input("Введите API-ключ io.net (опционально): ").strip()
        backuppath = input("Введите путь для резервных копий (по умолчанию ~/.config/psynclite/): ").strip()
        if not backuppath:
            backuppath = os.path.expanduser('~/.config/psynclite/')

        config = configparser.ConfigParser()
        config['GLOBAL'] = {'initialization': 'true'}
        config['AI'] = {'apikey': apikey}
        config['BACKUP'] = {'path': backuppath}

        with open(config_file, 'w') as f:
            config.write(f)

        print(f"\n✅ Конфигурация успешно создана: {config_file}")
        return 1
    except KeyboardInterrupt:
        return 0


# Ленивая загрузка конфигурации
CONFIG = read_config(FILE_CONFIG)