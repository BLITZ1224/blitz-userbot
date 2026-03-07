import google.generativeai as genai
import os

# API Key ကို .env ထဲကနေ လှမ်းဖတ်တာ (ဒါမှမှန်မှာ)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_key)

print("Checking available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Model Name: {m.name}")