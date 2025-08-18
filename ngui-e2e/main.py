import json
import os

from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from next_gen_ui_langgraph.agent import NextGenUILangGraphAgent
from langgraph.prebuilt import create_react_agent
from next_gen_ui_langgraph.readme_example import search_movie
from fastapi.middleware.cors import CORSMiddleware

# === Model Configuration ===
# 
# Configure your local AI model here. This example supports:
# 1. Ollama (default) - Local models via Ollama
# 2. OpenAI API - OpenAI's models
# 3. Other OpenAI-compatible APIs
#
# For Ollama (recommended for local development):
# 1. Install Ollama: https://ollama.ai/download
# 2. Pull a model: `ollama pull llama3.2:3b` (or any model you prefer)
# 3. Start Ollama: `ollama serve`
# 4. Update MODEL_NAME below to your preferred model
#
# Available Ollama models you can try:
# - llama3.2:3b (lightweight, good for development)
# - llama3.2:7b (better quality, requires more RAM)
# - llama3.1:8b (balanced performance)
# - codellama:7b (good for code-related tasks)
# - mistral:7b (alternative option)
#
# For OpenAI API:
# 1. Set OPENAI_API_KEY environment variable
# 2. Set MODEL_NAME to "gpt-3.5-turbo" or "gpt-4"
# 3. Set BASE_URL to None (or remove the base_url parameter)

# Model configuration - customize these values for your setup
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")  # Change this to your preferred model
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")  # Ollama default URL
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)  # Set this for OpenAI API

# === Setup ===
# Initialize the language model based on configuration
if OPENAI_API_KEY and BASE_URL is None:
    # Use OpenAI API
    llm = ChatOpenAI(model=MODEL_NAME, api_key=OPENAI_API_KEY)
elif BASE_URL:
    # Use Ollama or other OpenAI-compatible API
    llm = ChatOpenAI(model=MODEL_NAME, base_url=BASE_URL)
else:
    # Default Ollama setup
    llm = ChatOpenAI(model=MODEL_NAME, base_url="http://localhost:11434/v1")

# Important: use the tool function directly (not call it)
movies_agent = create_react_agent(
    model=llm,
    tools=[search_movie],
    prompt="You are useful movies assistant to answer user questions"
)

ngui_agent = NextGenUILangGraphAgent(model=llm).build_graph()
ngui_cfg = {"configurable": {"component_system": "json"}}

# === FastAPI setup ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_response(request: GenerateRequest):
    """
    Main API endpoint that processes user prompts and returns UI components.
    
    This endpoint:
    1. Takes a user prompt about movies
    2. Uses the movies agent to search for movie information
    3. Passes the response to the Next Gen UI agent to generate UI components
    4. Returns the UI component configuration as JSON
    
    You can customize this workflow by:
    - Changing the movies agent to handle different domains (books, music, etc.)
    - Modifying the prompt template
    - Adjusting the UI component generation logic
    """
    prompt = request.prompt
    print(f"Processing prompt: {prompt}")

    try:
        # Step 1: Invoke movies agent to get domain-specific data
        # NOTE: You can replace 'search_movie' with your own tools/functions
        movie_response = movies_agent.invoke({
            "messages": [{"role": "user", "content": prompt or "Give me details of toy story"}]
        })

        # Step 2: Pass to Next Gen UI agent to generate UI components
        # The agent converts the data into UI component configurations
        ngui_response = await ngui_agent.ainvoke(movie_response, ngui_cfg)

        # Debug: Print the generated UI configuration
        generated_ui = ngui_response["renditions"][0].content
        print(f"Generated UI configuration: {generated_ui}")

        # Step 3: Return UI response as JSON
        return {"response": json.loads(generated_ui)}
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {"error": f"Failed to process request: {str(e)}"}

# === Startup Information ===
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Next Gen UI API Server")
    print("=" * 60)
    print(f"📝 Model: {MODEL_NAME}")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"🔑 Using OpenAI API: {'Yes' if OPENAI_API_KEY else 'No'}")
    print("=" * 60)
    print("🎯 To start the server:")
    print("   uvicorn main:app --reload")
    print("")
    print("🎭 Available endpoints:")
    print("   POST /generate - Generate UI components from prompts")
    print("")
    print("🔧 To customize your model:")
    print("   1. Edit MODEL_NAME variable in this file")
    print("   2. Or set environment variables:")
    print("      export MODEL_NAME=your-model-name")
    print("      export BASE_URL=your-api-url")
    print("=" * 60)
