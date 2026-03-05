from setuptools import setup, find_packages

setup(
    name="ai-assistant-cli",
    version="0.1.0",
    description="Terminal AI assistant for developers",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich",
        "requests",
        "pypdf"
    ],
    entry_points={
        "console_scripts": [
            "ai=ai_cli.cli:app"
        ]
    },
)