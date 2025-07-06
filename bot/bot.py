from aiogram import Bot, Dispatcher, types

from bot.services.ai import AI
from bot.services.bot import BotService
from bot.services.language import TranslationsService

from .handlers import user


webhook_dp = Dispatcher()

webhook_dp["translation"] = TranslationsService()
webhook_dp["service"] = BotService()
webhook_dp["ai"] = AI()

webhook_dp.include_routers(user.router)


async def feed_update(token: str, update: dict):
    try:
        webhook_book = Bot(token=token)
        aiogram_update = types.Update(**update)
        await webhook_dp.feed_update(bot=webhook_book, update=aiogram_update)
    finally:
        await webhook_book.session.close()
