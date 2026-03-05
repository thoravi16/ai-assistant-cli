import json
from pathlib import Path
import os

CONFIG_FILE = Path.home() / ".ai_cli_config.json"

DEFAULT_CONFIG = {
    "model": "llama-3.1-8b-instant",
    "temperature": 0.3
}

def load_config():
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())

        try:
            config["temperature"] = float(config.get("temperature", 0.3))
        except:
            config["temperature"] = 0.3

        return config

    return DEFAULT_CONFIG


def save_config(key, value):
    config = load_config()

    if key == "temperature":
        try:
            value = float(value)
        except:
            value = 0.3

    config[key] = value
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def save_api_key(key):
    config = load_config()
    config["groq_api_key"] = key
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def get_api_key():
    config = load_config()
    return config.get("groq_api_key") or os.getenv("GROQ_API_KEY")