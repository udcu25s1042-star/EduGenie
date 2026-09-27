import asyncio
import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


async def generate_quiz(text: str):
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")

    model = genai.GenerativeModel(MODEL)
    prompt = (
        "Create a short 5-question multiple-choice quiz based on the provided text. "
        "Return valid JSON only in this format: "
        "[{\"question\":\"...\",\"options\":[\"A\",\"B\",\"C\",\"D\"],\"answer\":\"B\",\"explanation\":\"...\"}] "
        "Do not wrap the JSON in Markdown fences.\n\nText:\n"
        f"{text}"
    )

    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        raw_text = getattr(response, "text", "")
        cleaned = raw_text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()

        payload = json.loads(cleaned)
        if isinstance(payload, dict) and "questions" in payload:
            return payload["questions"]
        return payload
    except Exception as exc:
        raise RuntimeError(f"Failed to generate quiz: {exc}") from exc
