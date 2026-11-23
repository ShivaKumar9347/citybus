"""
Groq LLM Client Utility
"""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "qwen/qwen3.8-27b"


def ask_llm(prompt: str, system: str = "You are a helpful city bus operations assistant.") -> str:
    """Send a prompt to Groq LLM and return the response."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=512
    )
    return response.choices[0].message.content.strip()
