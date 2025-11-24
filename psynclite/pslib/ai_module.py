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
            print("API key found.")
            return api_key
        else:
            print("API key not found. Enter a new one:")

    api_key = input("Enter the API key for io.net: ").strip()
    set_value(FILE_CONFIG, CONFIG, 'AI', 'Apikey', api_key)
    print("API key is saved.")
    return api_key


def load_ai_model() -> str:
    """Load saved AI model or use default"""
    try:
        model = get_value(CONFIG, 'AI', 'model')
        if model == 1 or model == 2:
            print(f"{COLORS['red']}The model is not loaded! Error code: {model}{COLORS['reset']}")
            print(f"{COLORS['yellow']}Check the configuration file and run the {COLORS['reset']}{COLORS['green']}pscli -Ai model{COLORS['reset']} to set the model.{COLORS['reset']}")
            log("AI model not loaded. Code error: 1", 1, False)
            return 1
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
        print(f"{COLORS['red']}Error when getting the list of models: {e}{COLORS['reset']}")
        log(f"Failed to fetch models: {e}", 1, False)
        return 1

    models = [m['id'] for m in data.get('data', [])]
    if not models:
        print(f"{COLORS['yellow']}No models were found.{COLORS['reset']}")
        return 1

    print(f"\n{COLORS['green']}Available models:{COLORS['reset']}")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")

    while True:
        try:
            choice = int(input("\nEnter the model number: "))
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1]
                break
            print(f"{COLORS['red']}Incorrect number!{COLORS['reset']}")
        except ValueError:
            print(f"{COLORS['red']}Enter a number!{COLORS['reset']}")
        except KeyboardInterrupt:
            print(f"\n{COLORS['red']}The model selection was canceled by the user.{COLORS['reset']}")
            return

    set_value(FILE_CONFIG, CONFIG, 'AI', 'Model', selected_model)
    print(f"\n{COLORS['green']}The model {selected_model} сохраненis saved!{COLORS['reset']}")
    log("Model saved", 0, False)


def aiapi(argument) -> None:
    """Send AI request and print plain response"""

    api_key = get_api_key()
    model = load_ai_model()
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}

    if model == 1:
        return 1

    print(f"{COLORS['yellow']}The model used: {model}{COLORS['reset']}")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Jar — a helpful Linux assistant. "
                    "Respond clearly and concisely, avoid txt formatting."
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
            print(f"\n{COLORS['green']}AI's response:{COLORS['reset']}\n")
            print(answer.strip(), "\n")
        else:
            print(f"{COLORS['red']}Error: An empty response from the API.{COLORS['reset']}")

    except requests.exceptions.RequestException as e:
        print(f"{COLORS['red']}Network error: {e}{COLORS['reset']}")
        log("NetworkError", 1, True, "Network error when requesting the API")
    except json.JSONDecodeError:
        print(f"{COLORS['red']}Error decoding the API response.{COLORS['reset']}")
        log("DecodeError", 1, True, "JSON decoding error")
    except Exception as e:
        print(f"{COLORS['red']}Unknown error: {e}{COLORS['reset']}")
        log(f"Unexpected error: {e}", 1, True, "Unknown error in the request")
    else:
        log("AI response received successfully", 0, True, "The response from AI has been received")
