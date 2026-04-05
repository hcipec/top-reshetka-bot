import google.generativeai as genai
from config import GEMINI_API_KEY
from faq import build_system_prompt

genai.configure(api_key=GEMINI_API_KEY)

_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=build_system_prompt(),
)

# Пайдаланушы сессиялары: user_id → chat объектісі
_sessions: dict[int, genai.ChatSession] = {}


def get_session(user_id: int) -> genai.ChatSession:
    if user_id not in _sessions:
        _sessions[user_id] = _model.start_chat(history=[])
    return _sessions[user_id]


async def ask_gemini(user_id: int, message: str) -> str:
    session = get_session(user_id)
    try:
        response = session.send_message(message)
        return response.text
    except Exception as e:
        return f"Кешіріңіз, қазір жауап бере алмаймын. Менеджерге тікелей жазыңыз. (Қате: {type(e).__name__})"
