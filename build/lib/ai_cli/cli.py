import typer
from rich.console import Console
from ai_cli.ai_engine import ask_ai, summarize_text, explain_code, generate_command
from ai_cli.memory import add, get, clear, history
from ai_cli.config import load_config, save_config, save_api_key
from pypdf import PdfReader

app = typer.Typer()
console = Console()


@app.command()
def ask(query: str):

    messages = [{"role": "user", "content": query}]

    console.print("[green]AI:[/green] ", end="")
    ask_ai(messages)


@app.command()
def chat():

    console.print("\nAI Chat Mode (type 'exit', 'clear', 'history')\n")

    while True:

        user_input = console.input("You: ")

        if user_input.lower() == "exit":
            console.print("Exiting chat...")
            break

        if user_input.lower() == "clear":
            clear()
            console.print("Conversation cleared")
            continue

        if user_input.lower() == "history":
            for msg in history():
                console.print(msg)
            continue

        add("user", user_input)

        console.print("AI: ", end="")

        response = ask_ai(get())

        add("assistant", response)


@app.command()
def summarize(file: str):

    try:

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        console.print(f"\nSummarizing {file}...\n")

        summarize_text(text)

    except Exception as e:
        console.print(f"[Error] {e}")

@app.command()
def summarize_pdf(file: str):

    try:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        console.print(f"\nSummarizing PDF {file}...\n")

        summarize_text(text)

    except Exception as e:
        console.print(f"[Error] {e}")

@app.command()
def explain(code: str):

    console.print("\nExplaining code...\n")

    explain_code(code)


@app.command()
def cmd(task: str):

    console.print("\nGenerating command...\n")

    generate_command(task)


@app.command()
def config_show():

    console.print(load_config())


@app.command()
def config_set(key: str, value: str):

    save_config(key, value)
    console.print("Config updated")


@app.command()
def api_set(key: str):

    save_api_key(key)
    console.print("API key saved successfully")

@app.command()
def gitmsg():

    """
    Generate AI git commit message
    """

    import subprocess

    try:

        diff = subprocess.check_output(
            ["git", "diff", "--cached"],
            text=True
        )

        if not diff.strip():
            console.print("No staged changes found.")
            return

        prompt = f"""
Generate a clean git commit message for the following changes:

{diff}
"""

        messages = [{"role": "user", "content": prompt}]

        console.print("\nSuggested Commit Message:\n")

        ask_ai(messages)

    except Exception as e:
        console.print(f"[Error] {e}")

if __name__ == "__main__":
    app()