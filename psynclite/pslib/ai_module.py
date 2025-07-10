import requests
import os
import json
from .helpers import log
from .data import COLORS, FILE_CONFIG
from .formatters import MarkdownFormatter
from .config import get_value, set_value, check_parameter, CONFIG

def get_api_key():
    """Запрашивает и сохраняет API-ключ для io.net"""
    
    isApikey = check_parameter(CONFIG, 'AI', 'apikey', 'ExpectedValue')
    
    if isApikey == False or isApikey == True:
        api_key = get_value(CONFIG, 'AI', 'Apikey')
        if api_key:
            print("API-ключ найден.")
            return api_key
        else:
            print("API-ключ не найден в файле. Пожалуйста, введите новый.")

    api_key = input("Введите API-ключ для io.net: ")

    set_value(FILE_CONFIG, CONFIG, 'AI', 'Apikey', api_key)

    print("API-ключ сохранен.")
    return api_key
    
    

def load_ai_model():
    """Loading save AI model"""
    default_model = "mistralai/Mistral-Large-Instruct-2411"
    try:
        model = get_value(CONFIG, 'AI', 'model')
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
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    print(f"\n{COLORS['green']}Available models:{COLORS['reset']}")
    models = [model['id'] for model in data.get('data', [])]

    # Numeric list
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")

    # Choice model
    while True:
        try:
            choice = int(input("\nInput model number: "))
            if 1 <= choice <= len(models):
                selected_model = models[choice-1]
                break
            else:
                print(f"{COLORS['red']}Invalid number!{COLORS['reset']}")
        except ValueError:
            print(f"{COLORS['red']}Input number!{COLORS['reset']}")
            log("Invalid input", 1, False)
        except KeyboardInterrupt:
            print(f"\n{COLORS['red']}User aborted request{COLORS['reset']}")
            log("User aborted request", 1, False)
            exit(1)


    # Save in config
    set_value(FILE_CONFIG, CONFIG, 'AI', 'Model', selected_model)

    print(f"\n{COLORS['green']}Model {selected_model} is saved!{COLORS['reset']}")
    log("Model saved", 0, False)

def aiapi(argument):
    """Handling AI queries with full Markdown support"""
    api_key = get_api_key()
    current_model = load_ai_model()
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    formatter = MarkdownFormatter()

    print(f"{COLORS['yellow']}Используемая модель: {current_model}{COLORS['reset']}")
    try:
        data = {
            "model": current_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Jar - helpful assistant. Format all responses using Markdown. "
                        "You can use these elements:\n"
                        "- Headers (#, ##)\n"
                        "- Lists (ordered/unordered)\n"
                        "- **Bold** and *italic* text\n"
                        "- Code blocks (```) and `inline code`\n"
                        "- Links\n"
                        "- Blockquotes (>)\n"
                        "You always must answer clear and understandable, as for a beginner"
                    )
                },
                {"role": "user", "content": argument}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if 'choices' in result and result['choices']:
            raw_answer = result['choices'][0]['message']['content']
            formatted_answer = formatter.format(raw_answer)

            print(f"\n{COLORS['green']}AI Response:{COLORS['reset']}\n")
            for line in formatted_answer.split('\n'):
                print(f"  {line}")
            print()

        else:
            print(f"{COLORS['red']}Error: Invalid API response{COLORS['reset']}")

    except requests.exceptions.RequestException as e:
        print(f"{COLORS['red']}Error network: {e}{COLORS['reset']}")
        log("NetworkError", 1, True, "Couldn't send neural network request, check the Internet")
        exit(1)
    except json.JSONDecodeError:
        print(f"{COLORS['red']}Error decoding response{COLORS['reset']}")
        log("Error decoding response", 1, True, "Couldn't get a response from AI")
        exit(1)
    except Exception as e:
        print(f"{COLORS['red']}Unexpected error: {e}{COLORS['reset']}")
        log("Unexpected error", 1, True, "Couldn't get a response from AI")
        exit(1)
    log("AI response is good", 0, True, "The AI's response has been received")
