import requests
import json
import sys
from ai_cli.config import load_config, get_api_key

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OLLAMA_URL = "http://localhost:11434/api/chat"


def ask_ai(messages: list):

    api_key = get_api_key()
    config = load_config()

    #Safe default models
    groq_model = "llama-3.1-8b-instant"
    local_model = "tinyllama"

    temperature = float(config.get("temperature", 0.7))

    #GROQ API
    if api_key:
        print("\n[Using Groq API]\n")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": groq_model,
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
                stream=True,
                timeout=30
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

            else:
                print(f"[Groq Error {response.status_code}]")
                print(response.text)

        except Exception as e:
            print(f"[Groq Failed] {e}")

    else:
        print("\n[No API key → Using Local]\n")

    #OLLAMA FALLBACK
    try:
        print("\n[Using Local Ollama]\n")

        payload = {
            "model": local_model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": 250   #faster output
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=60
        )

        full_text = ""

        for line in response.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line.decode("utf-8"))
                content = data.get("message", {}).get("content", "")

                if content:
                    sys.stdout.write(content)
                    sys.stdout.flush()
                    full_text += content

            except:
                continue

        print()
        return full_text

    except Exception as e:
        print(f"[Ollama Error] {e}")
        print("\n Both Groq & Ollama failed")
        return ""


#FEATURES

def summarize_text(text):
    prompt = f"""
Summarize the following text clearly in bullet points.

TEXT:
{text}
"""
    return ask_ai([{"role": "user", "content": prompt}])


def explain_code(code):
    prompt = f"""
Explain the following code step-by-step like a senior developer.

CODE:
{code}
"""
    return ask_ai([{"role": "user", "content": prompt}])


def generate_command(task):
    prompt = f"""
Generate the best CLI command for the following task.

Task: {task}
"""
    return ask_ai([{"role": "user", "content": prompt}])


def generate_code(task):
    prompt = f"""
Write clean, production-ready code for the following task.

Task:
{task}
"""
    return ask_ai([{"role": "user", "content": prompt}])