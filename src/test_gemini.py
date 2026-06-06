from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Test it
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="Hello! Can you introduce yourself in 2 lines?"
)
print(response.text)