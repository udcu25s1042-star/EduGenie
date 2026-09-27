import asyncio
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


async def summarize_text(text: str) -> str:
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")

    model = genai.GenerativeModel(MODEL)
    prompt = (
        "Summarize the text efficiently while preserving the key ideas and important details. "
        "Keep the output concise but clear.\n\n"
        f"Text:\n{text}"
    )

    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        text_response = getattr(response, "text", "")
        return text_response.strip() if text_response else "No summary generated."
    except Exception as exc:
        raise RuntimeError(f"Failed to summarize text: {exc}") from exc
