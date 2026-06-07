from groq import Groq
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Test it
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Hello! Introduce yourself in 2 lines."}
    ]
)
print(response.choices[0].message.content)