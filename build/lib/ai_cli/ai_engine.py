import requests
import json
import sys
from ai_cli.config import load_config, get_api_key

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def ask_ai(messages: list):

    api_key = get_api_key()
    config = load_config()

    model = config["model"]
    temperature = float(config["temperature"])

    if api_key:

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 600,
            "stream": True
        }

        try:

            response = requests.post(
                GROQ_URL,
                headers=headers,
                json=payload,
                stream=True
            )

            if response.status_code == 200:

                full_text = ""

                for line in response.iter_lines():

                    if not line:
                        continue

                    decoded = line.decode("utf-8")

                    if not decoded.startswith("data: "):
                        continue

                    data = decoded.replace("data: ", "")

                    if data.strip() == "[DONE]":
                        break

                    try:

                        json_data = json.loads(data)
                        delta = json_data["choices"][0]["delta"]

                        if "content" in delta:
                            text = delta["content"]

                            sys.stdout.write(text)
                            sys.stdout.flush()

                            full_text += text

                    except:
                        continue

                print()
                return full_text

        except:
            pass


    # Ollama fallback
    try:

        print("\n[Using Local Ollama]\n")

        payload = {
            "model": "llama3",
            "messages": messages,
            "stream": True
        }

        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            stream=True
        )

        full_text = ""

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            content = data.get("message", {}).get("content", "")

            if content:
                sys.stdout.write(content)
                sys.stdout.flush()
                full_text += content

        print()
        return full_text

    except Exception as e:
        print(f"[Error] {e}")
        return ""


# ---- FEATURES ----

def summarize_text(text):

    prompt = f"""
Summarize the following text clearly in bullet points.

TEXT:
{text}
"""

    messages = [{"role": "user", "content": prompt}]
    return ask_ai(messages)


def explain_code(code):

    prompt = f"""
Explain the following code step-by-step like a senior developer.

CODE:
{code}
"""

    messages = [{"role": "user", "content": prompt}]
    return ask_ai(messages)


def generate_command(task):

    prompt = f"""
Generate the best CLI command for the following task.

Task: {task}

Explain the command briefly.
"""

    messages = [{"role": "user", "content": prompt}]
    return ask_ai(messages)