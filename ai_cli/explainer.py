from .ai_engine import ask_ai

def explain_command(command: str) -> str:
    prompt = f"Explain the following command in simple terms:\n{command}"
    return ask_ai(prompt)
