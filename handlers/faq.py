from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from faq import FAQ_LIST, FAQ_BY_ID

router = Router()

CONTACT_TEXT = (
    "📞 *Байланыс / Тапсырыс беру*\n\n"
    "Менеджерімізбен хабарласыңыз:\n\n"
    "👤 Telegram: @top_reshetka_manager\n"
    "📱 WhatsApp / Телефон: +7 (700) 000-00-00\n\n"
    "Тапсырыс беру үшін жіберіңіз:\n"
    "• Терезе өлшемі (ені × биіктігі)\n"
    "• Терезелер саны\n"
    "• Қала / мекенжай\n\n"
    "Менеджер *15 минут* ішінде жауап береді! 🚀"
)


def faq_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"❓ {item['question']}", callback_data=f"faq_{item['id']}")]
        for item in FAQ_LIST
    ]
    buttons.append([InlineKeyboardButton(text="🏠 Басты мәзір", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ FAQ тізіміне оралу", callback_data="faq_menu")],
            [InlineKeyboardButton(text="📞 Тапсырыс беру", callback_data="contact")],
        ]
    )


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❓ Жиі сұрақтар (FAQ)", callback_data="faq_menu")],
            [InlineKeyboardButton(text="💰 Баға білу", callback_data="faq_price")],
            [InlineKeyboardButton(text="📞 Байланыс / Тапсырыс", callback_data="contact")],
        ]
    )


@router.callback_query(lambda c: c.data == "faq_menu")
async def show_faq_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "❓ *Жиі қойылатын сұрақтар*\n\nҚызықтыратын сұрақты таңдаңыз:",
        parse_mode="Markdown",
        reply_markup=faq_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("faq_"))
async def show_faq_answer(callback: CallbackQuery) -> None:
    faq_id = callback.data.removeprefix("faq_")
    item = FAQ_BY_ID.get(faq_id)
    if not item:
        await callback.answer("Сұрақ табылмады", show_alert=True)
        return

    await callback.message.edit_text(
        f"*{item['question']}*\n\n{item['answer']}",
        parse_mode="Markdown",
        reply_markup=back_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "contact")
async def show_contact(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        CONTACT_TEXT,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Артқа", callback_data="back_main")]
            ]
        ),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_main")
async def back_to_main(callback: CallbackQuery) -> None:
    from handlers.start import WELCOME_TEXT
    await callback.message.edit_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )
    await callback.answer()
