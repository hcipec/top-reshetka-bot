from aiogram import Router
from aiogram.types import Message
from gemini_client import ask_gemini

router = Router()


@router.message()
async def handle_message(message: Message) -> None:
    if not message.text:
        return

    # Жазып жатыр индикаторы
    await message.bot.send_chat_action(message.chat.id, "typing")

    answer = await ask_gemini(message.from_user.id, message.text)
    await message.answer(answer, parse_mode="Markdown")
