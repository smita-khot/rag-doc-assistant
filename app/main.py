import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)

def main():
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": "Say hello and confirm you're working, in one sentence."}
        ]
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()