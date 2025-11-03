'''
import json
import logging
import os
import subprocess
import time
from collections import defaultdict
from .data import NOTIFICATION_HISTORY_FILE, COLORS

def log_notification(category, message, urgency='normal'):
    """Log notification and display it"""
    try:
        os.makedirs(os.path.dirname(NOTIFICATION_HISTORY_FILE), exist_ok=True)

        if not os.path.exists(NOTIFICATION_HISTORY_FILE) or \
           os.path.getsize(NOTIFICATION_HISTORY_FILE) == 0:
            history = []
        else:
            try:
                with open(NOTIFICATION_HISTORY_FILE, 'r') as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                print(f"{COLORS['yellow']}Error reading file history. Initializing new history.{COLORS['reset']}")
                history = []

        entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'message': message,
            'urgency': urgency
        }
        history.append(entry)
        history = history[-100:]  # Save 100 last

        temp_file = NOTIFICATION_HISTORY_FILE + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(history, f, indent=2)

        os.replace(temp_file, NOTIFICATION_HISTORY_FILE)

        subprocess.run([
            'notify-send',
            '-u', urgency,
            '-c', category,
            f'{category}',
            message
        ])

    except Exception as e:
        print(f"{COLORS['red']}Critical error loging: {e}{COLORS['reset']}")
        logging.exception("Critical error notify logging")

def show_notification_history(filter_category=None):
    """Show notification history with filter"""
    try:
        if not os.path.exists(NOTIFICATION_HISTORY_FILE) or \
           os.path.getsize(NOTIFICATION_HISTORY_FILE) == 0:
            print(f"{COLORS['yellow']}Notification history is empty{COLORS['reset']}")
            return

        with open(NOTIFICATION_HISTORY_FILE, 'r') as f:
                history = json.load(f)

        grouped = defaultdict(list)
        for entry in reversed(history):
            if not isinstance(entry, dict):  # Check structure
                continue
            if filter_category and entry.get('category') != filter_category:
                continue
            valid_entry = {
                'timestamp': entry.get('timestamp', 'Unknown'),
                'category': entry.get('category', 'Category is none'),
                'message': entry.get('message', 'None message')
            }
            grouped[valid_entry['category']].append(valid_entry)

        output = []
        for category, entries in grouped.items():
            output.append(f"{COLORS['yellow']}   {category}   {COLORS['reset']}")
            for entry in entries:
                time_str = entry['timestamp'].split()[1] if ' ' in entry['timestamp'] else entry['timestamp']
                output.append(
                    f"{COLORS['cyan']}{time_str}{COLORS['reset']} "
                    f"{entry['message']}"
                )
            output.append("")

        print('\n'.join(output) if output else f"{COLORS['yellow']}None records{COLORS['reset']}")

    except Exception as e:
        print(f"{COLORS['red']}Fatal error: {e}{COLORS['reset']}")
        logging.exception("Fatal error")
'''
import json
import logging
import os
import subprocess
import time
from collections import defaultdict
from .data import NOTIFICATION_HISTORY_FILE, COLORS


def log_notification(category, message, urgency='normal'):
    """Log notification and display it"""
    try:
        os.makedirs(os.path.dirname(NOTIFICATION_HISTORY_FILE), exist_ok=True)

        # Безопасная загрузка истории
        history = []
        if os.path.exists(NOTIFICATION_HISTORY_FILE) and os.path.getsize(NOTIFICATION_HISTORY_FILE) > 0:
            try:
                with open(NOTIFICATION_HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                if not isinstance(history, list):
                    raise ValueError("Invalid history structure")
            except (json.JSONDecodeError, ValueError):
                print(f"{COLORS['yellow']}Warning: corrupted history file, creating new one.{COLORS['reset']}")
                history = []

        # Добавляем новую запись
        entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'message': message,
            'urgency': urgency
        }
        history.append(entry)

        # Храним только последние 100
        history = history[-100:]

        # Безопасное сохранение (через временный файл)
        temp_file = NOTIFICATION_HISTORY_FILE + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(history, f, indent=2)
        os.replace(temp_file, NOTIFICATION_HISTORY_FILE)

        # Показ уведомления
        try:
            subprocess.run(
                ['notify-send', '-u', urgency, '-c', category, category, message],
                check=False
            )
        except FileNotFoundError:
            print(f"{COLORS['yellow']}Warning: notify-send not found{COLORS['reset']}")

    except Exception as e:
        print(f"{COLORS['red']}Critical error logging notification: {e}{COLORS['reset']}")
        logging.exception("Critical error in log_notification")


def show_notification_history(filter_category=None):
    """Show notification history with optional category filter"""
    try:
        if not os.path.exists(NOTIFICATION_HISTORY_FILE) or os.path.getsize(NOTIFICATION_HISTORY_FILE) == 0:
            print(f"{COLORS['yellow']}Notification history is empty{COLORS['reset']}")
            return

        with open(NOTIFICATION_HISTORY_FILE, 'r') as f:
            history = json.load(f)
        if not isinstance(history, list):
            print(f"{COLORS['yellow']}Corrupted history file{COLORS['reset']}")
            return

        grouped = defaultdict(list)
        for entry in reversed(history):
            if not isinstance(entry, dict):
                continue
            category = entry.get('category', 'Unknown')
            if filter_category and category != filter_category:
                continue
            grouped[category].append(entry)

        if not grouped:
            print(f"{COLORS['yellow']}No records found{COLORS['reset']}")
            return

        # Формируем вывод
        for category, entries in grouped.items():
            print(f"{COLORS['yellow']}   {category}   {COLORS['reset']}")
            for entry in entries:
                ts = entry.get('timestamp', 'Unknown')
                message = entry.get('message', 'No message')
                time_part = ts.split()[1] if ' ' in ts else ts
                print(f"{COLORS['cyan']}{time_part}{COLORS['reset']} {message}")
            print("")

    except Exception as e:
        print(f"{COLORS['red']}Fatal error: {e}{COLORS['reset']}")
        logging.exception("Fatal error in show_notification_history")