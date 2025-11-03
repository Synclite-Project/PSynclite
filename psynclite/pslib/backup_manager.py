import shutil
import os
import time
from .data import COLORS, CONFIG_DIR
from .config import get_value, set_value, CONFIG, FILE_CONFIG
from .helpers import log


def backup():
    """Backup utility in PSynclite for system"""
    print(f"\n{COLORS['yellow']}=== PSynclite Backup Utility ==={COLORS['reset']}")

    # Получаем путь из конфига
    backup_path = get_value(CONFIG, 'BACKUP', 'path')

    # Если секции нет или путь некорректный — создаём дефолтный
    if not backup_path or "not found" in str(backup_path).lower():
        default_path = os.path.expanduser('~/.config/psynclite/')
        print(f"{COLORS['yellow']}[!] Раздел [BACKUP] не найден, используется стандартный путь: {default_path}{COLORS['reset']}")
        set_value(FILE_CONFIG, CONFIG, 'BACKUP', 'path', default_path)
        backup_path = default_path

    # Приводим путь к абсолютному виду
    backup_path = os.path.expanduser(str(backup_path).strip())

    # Создаём подпапку с датой
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.join(backup_path, "backups", timestamp)

    try:
        os.makedirs(backup_dir, exist_ok=True)
    except Exception as e:
        print(f"{COLORS['red']}Не удалось создать директорию бэкапов: {e}{COLORS['reset']}")
        log("Failed to create backup directory", 1, True, str(e))
        return

    # Ввод путей
    paths_input = input(f"{COLORS['cyan']}Введите пути для бэкапа (через пробел): {COLORS['reset']}").strip()
    if not paths_input:
        print(f"{COLORS['yellow']}Бэкап отменён: пути не указаны.{COLORS['reset']}")
        log("Backup cancelled - no input paths", 1, False)
        return

    paths = [os.path.expanduser(p.strip()) for p in paths_input.split()]
    success, errors = [], []

    for path in paths:
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Путь не найден: {path}")

            if os.path.commonpath([path, backup_dir]) == backup_dir:
                raise ValueError("Попытка копирования каталога бэкапов внутрь самого себя")

            dest = os.path.join(backup_dir, os.path.basename(path))

            if os.path.isdir(path):
                shutil.copytree(path, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(path, dest)

            success.append(f"{path} → {dest}")

        except Exception as e:
            errors.append(f"{path}: {str(e)}")

    # Отчёт
    print(f"\n{COLORS['green']}=== Backup Report ==={COLORS['reset']}")
    print(f"{COLORS['bold']}Backup location:{COLORS['reset']} {backup_dir}")

    if success:
        print(f"\n{COLORS['green']}Успешно скопировано:{COLORS['reset']}")
        for item in success:
            print(f"  • {item}")

    if errors:
        print(f"\n{COLORS['red']}Ошибки при копировании:{COLORS['reset']}")
        for error in errors:
            print(f"  • {error}")

    status = "успешно" if not errors else "с ошибками"
    print(f"\n{COLORS['cyan']}Бэкап завершён {status}.{COLORS['reset']}")

    if errors:
        log("Backup completed with errors", 1, True, f"{len(errors)} errors")
    else:
        log("Backup completed successfully", 0, True, "All files copied successfully")
