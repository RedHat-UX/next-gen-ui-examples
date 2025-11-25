# Next Gen UI Examples - Streamlit

Next Gen UI examples powered by Streamlit UI

* `movies_llama_stack_app.py` - Movies assistent powered by Llama Stack
* `movies_langgraph_app.py` - Movies assistent powered by Lang Graph

## Setup 

### Python setup

Setup virtual env:
```sh
cd streamlit
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```sh
pip install -r requirements.txt
```

Alternativelly you can install local build of Next Gen UI from `dist` directory:
```sh
pip uninstall -y ../../next-gen-ui-agent/dist/next_gen_ui*.whl
pip install ../../next-gen-ui-agent/dist/next_gen_ui*.whl
# and install again other deps:
pip install -r requirements.txt
```

### Ollama setup

Install [Ollama server](https://ollama.com/download).

Pull `llama3.2:latest` model
```sh
ollama pull llama3.2:latest
ollama list
```

## LangGraph Examples

There is nothing to set up. Just run the example.

### Run Streamlit LangGraph App

```sh
streamlit run movies_langgraph_app.py
```

## Llama-stack Examples

### Llama-stack setup

Run Ollama model
```sh
export OLLAMA_INFERENCE_MODEL="llama3.2:3b-instruct-fp16"
ollama run $OLLAMA_INFERENCE_MODEL --keepalive 60m
```

Start Llama-stack server
```sh
export LLAMA_STACK_PORT=8321
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"

podman run -it --rm \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama:z \
  llamastack/distribution-ollama:0.1.9 \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env OLLAMA_URL=http://host.containers.internal:11434
```
Use `--env OLLAMA_URL=http://host.docker.internal:11434` if using docker.


### Run Streamlit Llama Stack App

```sh
streamlit run movies_llama_stack_app.py
```
