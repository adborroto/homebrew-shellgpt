#!/usr/bin/env python3
import argparse
import subprocess
import sys


def save_to_defaults(domain, key, value):
    """Save a value to macOS defaults."""
    subprocess.run(["defaults", "write", domain, key, value], check=True)


def read_from_defaults(domain, key):
    """Read a value from macOS defaults."""
    try:
        result = subprocess.check_output(
            ["defaults", "read", domain, key], text=True
        ).strip()
        return result
    except subprocess.CalledProcessError:
        return None


def init_config(api_key, model):
    """Initialize the configuration."""
    domain = "com.shellgpt.settings"
    save_to_defaults(domain, "APIKey", api_key)
    save_to_defaults(domain, "DefaultModel", model)
    print("Configuration saved successfully.")


def load_config():
    """Load configuration from macOS defaults."""
    domain = "com.shellgpt.settings"
    api_key = read_from_defaults(domain, "APIKey")
    model = read_from_defaults(domain, "DefaultModel")
    if not api_key or not model:
        raise ValueError("Configuration not found. Use 'shellgpt init' first.")
    return {"api_key": api_key, "default_model": model}


def query_openai(prompt, model, api_key):
    """Send a prompt to OpenAI API using the updated API."""
    try:
        import openai

        client = openai.OpenAI(
            api_key=api_key,
        )
        context = ""

        if not sys.stdin.isatty():
            context = sys.stdin.read().strip()

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ]
        response = client.chat.completions.create(model=model, messages=messages)
        response_message = response.choices[0].message
        print(response_message.content.strip())

    except Exception as e:
        print(f"Unexpected error: {e}")


def execute_command(command):
    """Execute a shell command and return its output."""
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing the command: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="ShellGPT: Interact with OpenAI from the shell"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the configuration")
    init_parser.add_argument("-key", help="API key de OpenAI")
    init_parser.add_argument(
        "-model",
        help="Default model to use(e.g., gpt-3.5-turbo)",
        default="gpt-4o-mini",
    )

    # Model command
    model_parser = subparsers.add_parser("model", help="Check the default model")

    # Query prompt
    prompt_parser = subparsers.add_parser("p", help="Send a prompt to OpenAI")
    prompt_parser.add_argument("prompt", help="Prompt to send to OpenAI")

    args = parser.parse_args()

    if args.command == "init":
        init_config(args.key, args.model)
    elif args.command == "p":
        config = load_config()
        query_openai(args.prompt, config["default_model"], config["api_key"])
    elif args.command == "model":
        config = load_config()
        print(f"Default model: {config['default_model']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
