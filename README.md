# shellgpt

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Homebrew](https://img.shields.io/badge/Homebrew-Tap-orange)](https://brew.sh)

**ShellGPT** is a command-line tool that allows you to interact seamlessly with OpenAI's GPT models directly from your shell. With this tool, you can send prompts, retrieve AI-powered completions, and manage configurations—all without leaving your terminal.

---

## 🚀 Features

- **Effortless AI interaction**: Query OpenAI's GPT models directly from your shell.
- **Configurable settings**: Save and manage your OpenAI API key and default model for a streamlined experience.
- **Simple installation**: Install and manage the tool via Homebrew for macOS.
- **Extensible**: Built with Python, easily customizable for advanced users.

---

## 📦 Installation

First, ensure you have [Homebrew](https://brew.sh) installed on your macOS.

### Add the Tap

To install ShellGPT using Homebrew, add the custom tap:

```bash
brew tap adborroto/shellgpt
brew install shellgpt
```

## 🛠️ Configuration

Before using ShellGPT, you must configure it with your OpenAI API key:

Initialize Configuration

```bash
shellgpt init -key YOUR_API_KEY -model gpt-3.5-turbo
```

Replace YOUR_API_KEY with your actual OpenAI API key. The default model is set to gpt-4o-mini. You can specify other models, such as gpt-4, during initialization.

## 🧑‍💻 Usage

### Send a Prompt

To interact with OpenAI's GPT models, use:

```bash
shellgpt p "What is the capital of France?"
```

### Check the Default Model

You can verify the configured default model:

```bash
shellgpt model
```

### Advanced Example

Pipe input from another command into `shellgpt`:

```bash
cat book.txt | shellgpt p "Make a summary"
```

## 📝 License

This project is licensed under the MIT License. Feel free to use and adapt it as needed.

## 🛡️ Support

If you encounter any issues or have questions, feel free to open an issue in this repository.


## Release

```
git tag -a vx.x.x -m "Release vx.x.x"   
git archive --format=tar.gz --output=shellgpt-vx.x.x.tar.gz vx.x.x
shasum -a 256 shellgpt-vx.x.x.tar.gz
git push origin --tags 
```
Modify `shellgpt.rb` with the SHA version
