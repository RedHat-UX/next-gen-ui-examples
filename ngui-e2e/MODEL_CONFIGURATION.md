# Model Configuration Guide

This guide explains how to configure your own AI model for the Next Gen UI API.

## Quick Start

The API is pre-configured to work with Ollama and `llama3.2:3b`. To get started:

1. Install Ollama: https://ollama.ai/download
2. Pull the model: `ollama pull llama3.2:3b`
3. Start the server: `uvicorn main:app --reload`

## Configuration Options

### Option 1: Edit main.py directly

Open `main.py` and modify these lines:

```python
MODEL_NAME = "your-preferred-model"    # Line ~39
BASE_URL = "your-api-url"              # Line ~40
```

### Option 2: Use Environment Variables

Set environment variables before starting the server:

```bash
export MODEL_NAME=llama3.2:7b
export BASE_URL=http://localhost:11434/v1
uvicorn main:app --reload
```

## Supported Models

### Ollama Models (Recommended for local development)

```bash
# Lightweight - good for development
ollama pull llama3.2:3b

# Better quality - requires more RAM
ollama pull llama3.2:7b

# Balanced performance
ollama pull llama3.1:8b

# Good for code-related tasks
ollama pull codellama:7b

# Alternative option
ollama pull mistral:7b
```

### OpenAI API

```bash
export MODEL_NAME=gpt-3.5-turbo
export OPENAI_API_KEY=your-api-key
export BASE_URL=  # Leave empty for OpenAI
```

### Other OpenAI-Compatible APIs

For services like LocalAI, Oobabooga, vLLM, etc.:

```bash
export MODEL_NAME=your-model-name
export BASE_URL=http://your-api-url/v1
```

## Testing Your Configuration

1. Start the server: `uvicorn main:app --reload`
2. Check the startup messages for your model configuration
3. Test with curl:

```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Tell me about Toy Story"}'
```

## Troubleshooting

- **Model not found**: Ensure your model is pulled/available
- **Connection refused**: Check if your model server is running
- **API key issues**: Verify your API key is set correctly
- **Memory issues**: Try a smaller model like `llama3.2:3b`

## Performance Tips

- For development: Use `llama3.2:3b` (fastest)
- For quality: Use `llama3.2:7b` or `llama3.1:8b`
- For production: Consider using OpenAI API or a dedicated server
