from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash klaviaturasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            ],
        ],
    )
