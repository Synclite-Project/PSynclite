import requests
import os
import json
from .helpers import log
from .data import COLORS, FILE_CONFIG
from .config import get_value, set_value, check_parameter, CONFIG


def get_api_key() -> str:
    """Request and save API key for io.net"""
    isApikey = check_parameter(CONFIG, 'AI', 'apikey', 'ExpectedValue')

    if isApikey in (False, True):
        api_key = get_value(CONFIG, 'AI', 'Apikey')
        if api_key:
            print("API-ключ найден.")
            return api_key
        else:
            print("API-ключ не найден. Введите новый:")

    api_key = input("Введите API-ключ для io.net: ").strip()
    set_value(FILE_CONFIG, CONFIG, 'AI', 'Apikey', api_key)
    print("API-ключ сохранён.")
    return api_key


def load_ai_model() -> str:
    """Load saved AI model or use default"""
    default_model = "deepseek-ai/DeepSeek-R1-0528"
    try:
        model = get_value(CONFIG, 'AI', 'model')
        return model or default_model
    except FileNotFoundError:
        log("AI model file not found, install with -am", 1, False)
        return default_model
    except Exception as e:
        print(f"{COLORS['yellow']}Error loading AI model: {e}, using default model{COLORS['reset']}")
        log("Error loading AI model", 1, False)
        return default_model


def aimodel():
    """Model choice for AI requests"""
    api_key = get_api_key()
    url = "https://api.intelligence.io.solutions/api/v1/models"
    headers = {"accept": "application/json", "Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"{COLORS['red']}Ошибка при получении списка моделей: {e}{COLORS['reset']}")
        log(f"Failed to fetch models: {e}", 1, False)
        return 1

    models = [m['id'] for m in data.get('data', [])]
    if not models:
        print(f"{COLORS['yellow']}Модели не найдены.{COLORS['reset']}")
        return 1

    print(f"\n{COLORS['green']}Доступные модели:{COLORS['reset']}")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")

    while True:
        try:
            choice = int(input("\nВведите номер модели: "))
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1]
                break
            print(f"{COLORS['red']}Некорректный номер!{COLORS['reset']}")
        except ValueError:
            print(f"{COLORS['red']}Введите число!{COLORS['reset']}")
        except KeyboardInterrupt:
            print(f"\n{COLORS['red']}Выбор модели отменён пользователем.{COLORS['reset']}")
            return

    set_value(FILE_CONFIG, CONFIG, 'AI', 'Model', selected_model)
    print(f"\n{COLORS['green']}Модель {selected_model} сохранена!{COLORS['reset']}")
    log("Model saved", 0, False)


def aiapi(argument) -> None:
    """Send AI request and print plain response"""
    api_key = get_api_key()
    model = load_ai_model()
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"{COLORS['yellow']}Используемая модель: {model}{COLORS['reset']}")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Jar — a helpful Linux assistant. "
                    "Respond clearly and concisely, avoid Markdown formatting."
                ),
            },
            {"role": "user", "content": argument},
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and result["choices"]:
            answer = result["choices"][0]["message"]["content"]
            print(f"\n{COLORS['green']}Ответ AI:{COLORS['reset']}\n")
            print(answer.strip(), "\n")
        else:
            print(f"{COLORS['red']}Ошибка: Пустой ответ от API.{COLORS['reset']}")

    except requests.exceptions.RequestException as e:
        print(f"{COLORS['red']}Ошибка сети: {e}{COLORS['reset']}")
        log("NetworkError", 1, True, "Ошибка сети при запросе к API")
    except json.JSONDecodeError:
        print(f"{COLORS['red']}Ошибка декодирования ответа API.{COLORS['reset']}")
        log("DecodeError", 1, True, "Ошибка декодирования JSON")
    except Exception as e:
        print(f"{COLORS['red']}Неизвестная ошибка: {e}{COLORS['reset']}")
        log(f"Unexpected error: {e}", 1, True, "Неизвестная ошибка при запросе")
    else:
        log("AI response received successfully", 0, True, "Ответ от AI получен")
