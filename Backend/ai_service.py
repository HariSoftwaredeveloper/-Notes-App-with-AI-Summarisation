# backend/ai_service.py
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv() # Load environment variables

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Initialize the Azure OpenAI Client outside the function for efficiency
if all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
    try:
        AZURE_CLIENT = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION
        )
    except Exception as e:
        print(f"Error initializing AzureOpenAI Client: {e}")
        AZURE_CLIENT = None
else:
    print("Warning: Azure OpenAI credentials not fully configured.")
    AZURE_CLIENT = None

def summarize_text(text: str) -> str:
    """Calls Azure OpenAI GPT-4o model to generate a summary."""
    if not AZURE_CLIENT:
        return "AI Service is offline (Configuration Error)."
    
    if len(text) < 50:
        return "Content too short to summarize (min 50 characters)."

    system_prompt = "You are a professional summarization assistant. Provide a concise, 1-3 sentence summary of the following text."
    
    try:
        response = AZURE_CLIENT.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.1,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Azure OpenAI Error: {e}")
        return f"AI summarization failed due to API error: {e}"
