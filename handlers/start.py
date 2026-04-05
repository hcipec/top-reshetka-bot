from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

WELCOME_TEXT = (
    "👋 Сәлем! *ТОП РЕШЕТКА* ботына қош келдіңіз!\n\n"
    "🛡 Біз балаларды терезеден құлап кетуден қорғайтын *болат решеткалар* орнатамыз.\n\n"
    "✅ Кез-келген терезе өлшеміне\n"
    "✅ Орнату 1-3 күн ішінде\n"
    "✅ 5 жыл гарантия\n"
    "✅ Баға 15 000 ₸-дан\n\n"
    "Төменгі батырмаларды пайдаланыңыз немесе кез-келген сұрағыңызды жазыңыз 👇"
)


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❓ Жиі сұрақтар (FAQ)", callback_data="faq_menu")],
            [InlineKeyboardButton(text="💰 Баға білу", callback_data="faq_price")],
            [InlineKeyboardButton(text="📞 Байланыс / Тапсырыс", callback_data="contact")],
        ]
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )
