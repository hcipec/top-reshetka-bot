import asyncio
import logging

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from config import GEMINI_API_KEY
from faq import build_system_prompt

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=build_system_prompt(),
)

# Пайдаланушы сессиялары: user_id → chat объектісі
_sessions: dict[int, genai.ChatSession] = {}


def get_session(user_id: int) -> genai.ChatSession:
    if user_id not in _sessions:
        _sessions[user_id] = _model.start_chat(history=[])
    return _sessions[user_id]


def _send_sync(session: genai.ChatSession, message: str) -> str:
    return session.send_message(message).text


async def ask_gemini(user_id: int, message: str) -> str:
    session = get_session(user_id)
    for attempt in range(3):
        try:
            return await asyncio.to_thread(_send_sync, session, message)
        except ResourceExhausted:
            if attempt < 2:
                wait = (attempt + 1) * 2
                logger.warning("ResourceExhausted, %s секунд күтіп retry...", wait)
                await asyncio.sleep(wait)
            else:
                return "Сұраныстар тым көп, бірнеше секундтан соң қайталап көріңіз."
        except Exception as e:
            logger.error("Gemini error: %s", e)
            return "Кешіріңіз, қазір жауап бере алмаймын. Менеджерге тікелей жазыңыз."
