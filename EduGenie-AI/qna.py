import asyncio
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


async def answer_question(question: str) -> str:
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")

    model = genai.GenerativeModel(MODEL)
    prompt = (
        "Answer this educational question clearly and accurately. "
        "Use a student-friendly tone and explain steps whenever useful.\n\n"
        f"Question: {question}"
    )

    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        text = getattr(response, "text", "")
        return text.strip() if text else "No answer generated."
    except Exception as exc:
        raise RuntimeError(f"Failed to answer question: {exc}") from exc
