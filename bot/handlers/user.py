from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards.user import get_language_keyboard
from bot.models import BotUser
from bot.services.ai import AI
from bot.services.bot import BotService
from bot.services.language import TranslationsService


router = Router()


@router.message(Command("start"))
async def start_command(message: Message, service: BotService, translation: TranslationsService):
    from_user = message.from_user

    user: BotUser = await service.get_create_user(
        telegram_id=from_user.id,
        username=from_user.username,
        first_name=from_user.first_name,
        last_name=from_user.last_name,
    )

    await message.answer(
        translation.get_text("hello", lang=user.language).format(user.first_name),
        reply_markup=get_language_keyboard(),
    )


@router.callback_query(lambda c: c.data.startswith("lang_"))
async def language_callback(callback: CallbackQuery, service: BotService, translation: TranslationsService):
    """Til tanlash callback"""
    lang = callback.data.split("_")[1]

    await service.set_user_lang(callback.from_user.id, lang)
    await callback.message.edit_text(translation.get_text("language_selected", lang))


@router.message()
async def handle_message(message: Message, ai: AI, service: BotService):
    loading = await message.answer("⏳")

    lang = await service.get_user_lang(message.from_user.id)
    message_text = message.text

    old_messages = await service.get_user_messages(message.from_user.id)

    await service.create_chat_message(
        telegram_id=message.from_user.id,
        role="user",
        content=message_text,
    )

    response = await ai.send_prompt(
        text=message_text,
        lang=lang,
        old_messages=old_messages,
    )

    await service.create_chat_message(
        telegram_id=message.from_user.id,
        role="assistant",
        content=response,
    )

    if len(response) > 4096:
        response = response[:4093] + "..."

    try:
        await message.answer(response, parse_mode="MARKDOWN")

    except Exception:
        await message.answer(response)

    await loading.delete()
