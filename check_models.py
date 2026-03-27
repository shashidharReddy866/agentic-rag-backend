import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key starts with: {api_key[:5] if api_key else 'None'}")

if api_key == "your_api_key_goes_here" or api_key == "your_api_key_here" or not api_key:
    print("CRITICAL: Using placeholder or missing API key!")
else:
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print("Available models for this key:")
        for m in models:
            print("- " + m)
    except Exception as e:
        print("API Error:", str(e))
