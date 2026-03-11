import json
import os

from dotenv import load_dotenv
from google import genai

from app.prompts import ROUTER_SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def call_llm(question: str) -> dict:

    prompt = f"""
{ROUTER_SYSTEM_PROMPT}

User query:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    # Clean markdown code fences if Gemini adds them
    if text.startswith("```json"):
        text = text.removeprefix("```json").removesuffix("```").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").removesuffix("```").strip()

    return json.loads(text)