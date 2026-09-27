import asyncio
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


async def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")

    model = genai.GenerativeModel(MODEL)
    prompt = (
        "Create a practical study plan for the given topic and learner level. "
        "Give a clear sequence of steps, resources, and milestones.\n\n"
        f"Topic: {topic}\nLevel: {level}"
    )

    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        text = getattr(response, "text", "")
        return text.strip() if text else "No learning recommendations generated."
    except Exception as exc:
        raise RuntimeError(f"Failed to generate learning recommendations: {exc}") from exc
