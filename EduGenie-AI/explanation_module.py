import asyncio
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


async def explain_concept(topic: str) -> str:
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")

    model = genai.GenerativeModel(MODEL)
    prompt = (
        "Explain the topic in a simple, engaging, and educational way. "
        "Use clear examples and define the key concept before going deeper.\n\n"
        f"Topic: {topic}"
    )

    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        text = getattr(response, "text", "")
        return text.strip() if text else "No explanation generated."
    except Exception as exc:
        raise RuntimeError(f"Failed to explain concept: {exc}") from exc
