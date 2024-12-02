# HackerNews Article Summarizer

A Python application that fetches top articles from Hacker News, generates summaries using a local LLM (Llama) via Ollama, and exports them to Excel for easy reading.

## Features

- 🔄 Fetches top stories from Hacker News API
- 📝 Generates article summaries using local Llama model via Ollama
- 📊 Exports summaries to Excel with article links and metadata
- 🗃️ Stores article data in SQLite database
- ⏰ Runs on a configurable schedule

## Prerequisites

- Python 3.11+
- Ollama installed and running locally
- Llama3.2 model pulled in Ollama

### Installing Ollama and Llama3.2

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the Llama3.2 model:
```bash
ollama pull llama3.2:3b-instruct-q4_K_M 
```

## Running the Application

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. To install and run the project using uv:

1. Install uv: https://docs.astral.sh/uv/getting-started/installation/

2. Run python:
```bash
uv run app.py
```
