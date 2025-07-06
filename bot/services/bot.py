from bot.models import BotUser, ChatMessage
from bot.services.language import TranslationsService

from asgiref.sync import sync_to_async


class BotService:

    async def get_user_lang_code(self, telegram_id):
        try:
            user = await BotUser.objects.aget(telegram_id=telegram_id)
            return user.language

        except BotUser.DoesNotExist:
            return TranslationsService.UZ

    async def get_user_lang(self, telegram_id):
        try:
            user = await BotUser.objects.aget(telegram_id=telegram_id)
            return user.get_language_display()

        except BotUser.DoesNotExist:
            return TranslationsService.UZ

    async def get_create_user(self, *, telegram_id, username, first_name, last_name):
        user, created = await BotUser.objects.aget_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "language": TranslationsService.UZ,
            },
        )

        return user

    async def set_user_lang(self, telegram_id, lang):
        user = await BotUser.objects.aget(telegram_id=telegram_id)

        user.language = lang
        await user.asave()

    async def create_chat_message(self, *, telegram_id, role, content):
        user = await BotUser.objects.aget(telegram_id=telegram_id)

        message = await ChatMessage.objects.acreate(user=user, role=role, content=content)
        return message

    @sync_to_async
    def get_user_messages(self, telegram_id):
        user = BotUser.objects.get(telegram_id=telegram_id)

        messages = ChatMessage.objects.filter(user=user).order_by("created_at").values_list("role", "content")

        return [{"role": role, "content": content} for role, content in messages]
