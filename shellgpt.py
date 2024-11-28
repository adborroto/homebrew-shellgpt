#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import json

model_ids = [
    "gpt-4",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "gpt-3.5",
    "gpt-4o",
    "gpt-4o-mini",
    "o1-preview",
    "o1-mini",
]

TEMPLATE_FILE = "shellgpt_templates.json"

def _create_openai_client(api_key: str):
    """Create and return an OpenAI client instance."""
    import openai
    return openai.OpenAI(api_key=api_key)

def _save_to_defaults(domain, key, value):
    """Save a value to macOS defaults."""
    subprocess.run(["defaults", "write", domain, key, value], check=True)

def _load_templates() -> dict:
    """Load templates from a JSON file."""
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r") as file:
            return json.load(file)
    return {}

def _save_templates(templates: dict):
    """Save templates to a JSON file."""
    with open(TEMPLATE_FILE, "w") as file:
        json.dump(templates, file, indent=4)


def _read_from_defaults(domain, key):
    """Read a value from macOS defaults."""
    try:
        result = subprocess.check_output(
            ["defaults", "read", domain, key], text=True
        ).strip()
        return result
    except subprocess.CalledProcessError:
        return None


def _load_config():
    """Load configuration from macOS defaults."""
    domain = "com.shellgpt.settings"
    api_key = _read_from_defaults(domain, "APIKey")
    model = _read_from_defaults(domain, "DefaultModel")
    if not api_key or not model:
        raise ValueError("Configuration not found. Use 'shellgpt init' first.")
    return {"api_key": api_key, "default_model": model}


def _query_openai(prompt, model, api_key):
    """Send a prompt to OpenAI API using the updated API."""
    try:
        client = _create_openai_client(api_key)
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


def model_command(args):
    if args.set:
        _save_to_defaults("com.shellgpt.settings", "DefaultModel", args.set)
        print(f"Default model set to {args.set}")
    elif args.list:
        print("Available models:")
        for model in model_ids:
            print(model)
    else:
        config = _load_config()
        print(f"Default model: {config['default_model']}")


def prompt_command(args):
    config = _load_config()
    model = args.model or config["default_model"]
    if args.template:
        templates = _load_templates()
        if args.template not in templates:
            print(f"Template '{args.template}' not found. Use 'shellgpt template --list' to see all templates.")
            return
        _query_openai(templates[args.template], model, config["api_key"])
    else:
        _query_openai(args.prompt, model, config["api_key"])


def init_command(api_key, model):
    """Initialize the configuration."""
    domain = "com.shellgpt.settings"
    _save_to_defaults(domain, "APIKey", api_key)
    _save_to_defaults(domain, "DefaultModel", model)
    print("Configuration saved successfully.")

def chat_command(args):
    """Start a chat session with OpenAI."""
    config = _load_config()
    model = args.model or config["default_model"]
    api_key = config["api_key"]

    try:
        client = _create_openai_client(api_key)
        context = ""

        if not sys.stdin.isatty():
            context = sys.stdin.read().strip()

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": "Start of chat session."},
        ]

        print("Starting chat session. Type 'exit' to end the session.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Ending chat session.")
                break

            messages.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(model=model, messages=messages)
            response_message = response.choices[0].message
            print(f"ChatGPT: {response_message.content.strip()}")
            messages.append({"role": "assistant", "content": response_message.content.strip()})

    except Exception as e:
        print("Chat endended.")

def template_command(args):
    """Handle template operations."""
    templates = _load_templates()
    if args.new:
        if args.new in templates:
            print(f"Template '{args.new}' already exists. Use 'shellgpt template --list' to see all templates.")
            return
        if not args.prompt:
            print("Please provide a prompt for the new template.")
            return
        
        templates[args.new] = args.prompt
        _save_templates(templates)
        print(f"Template '{args.new}' saved successfully.")
    elif args.list:
        if not templates:
            print("No templates found.")
            print("Use 'shellgpt template --new <template_name> --prompt <prompt>' to create a new template.")
            return
        print("Available templates:")
        for name, prompt in templates.items():
            print(f"{name}: {prompt}")
        print("Use 'shellgpt p --template <template_name>' to use a template.")
    



def main():
    parser = argparse.ArgumentParser(
        description="shellgpt: Interact with ChatGPT from the shell"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the configuration")
    init_parser.add_argument("-k", "--key", help="API key de OpenAI")
    init_parser.add_argument(
        "-m",
        "--model",
        help="Default model to use(e.g., gpt-3.5-turbo)",
        default="gpt-4o-mini",
    )

    # Model command
    model_parser = subparsers.add_parser("model", help="Check the default model")
    model_parser.add_argument("-s", "--set", help="Set the default model")
    model_parser.add_argument("-l", "--list", action="store_true", help="List all available models from ChatGPT")

    # Query prompt
    prompt_parser = subparsers.add_parser("p", help="Send a prompt to OpenAI")
    prompt_parser.add_argument(
       "-t", "--template", help="Use a template for the prompt"
    )
    prompt_parser.add_argument(
        "-m", "--model", help="Model to use (e.g., gpt-3.5-turbo)"
    )
    prompt_parser.add_argument("prompt", help="Prompt to send to OpenAI", nargs="?")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start a chat session with OpenAI")
    chat_parser.add_argument(
        "-m", "--model", help="Model to use for the chat session (e.g., gpt-3.5-turbo)"
    )

    # Template command
    template_parser = subparsers.add_parser("templates", help="Manage templates")
    template_parser.add_argument("--new", help="Create a new template")
    template_parser.add_argument("--prompt", help="Prompt for the new template")
    template_parser.add_argument("--list", action="store_true", help="List all templates")

    args = parser.parse_args()

    if args.command == "init":
        init_command(args.key, args.model)
    elif args.command == "p":
        prompt_command(args)
    elif args.command == "model":
        model_command(args)
    elif args.command == "chat":
        chat_command(args);
    elif args.command == "templates":
        template_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit(1)
