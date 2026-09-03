import httpx
import json
import logging
from backend.config import settings

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_llm(system_prompt: str, user_prompt: str) -> dict:
    api_key = settings.GROQ_API_KEY
    if not api_key:
        logger.warning("GROQ_API_KEY not set. Using fallback analysis.")
        return {"error": "AI service not configured. Please set GROQ_API_KEY."}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 2048,
        "response_format": {"type": "json_object"},
    }

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(GROQ_API_URL, json=payload, headers=headers)
            logger.info(f"Groq API response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
    except httpx.HTTPStatusError as e:
        logger.error(f"Groq API HTTP error: {e.response.status_code} - {e.response.text}")
        return {"error": f"AI service error: {e.response.status_code}"}
    except Exception as e:
        logger.error(f"Groq API call failed: {str(e)}")
        return {"error": f"AI service unavailable: {str(e)}"}
