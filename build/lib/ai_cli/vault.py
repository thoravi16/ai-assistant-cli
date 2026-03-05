import json
from pathlib import Path

VAULT = Path.home() / ".ai_recipes.json"

def load():
    if VAULT.exists():
        return json.loads(VAULT.read_text())
    return {}

def save(name, command):
    data = load()
    data[name] = command
    VAULT.write_text(json.dumps(data, indent=2))
    return "Saved."

def search(keyword):
    data = load()
    return {k:v for k,v in data.items() if keyword.lower() in k.lower()}