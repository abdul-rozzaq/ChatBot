import redis

from django.conf import settings

from datetime import datetime

from zoneinfo import ZoneInfo

from bot.models import BotUser, ChatMessage
from bot.services.language import TranslationsService

from asgiref.sync import sync_to_async


redis = redis.Redis.from_url(settings.REDIS_URL)
tz = ZoneInfo("Asia/Tashkent")


class BotService:
    TTL_SECONDS = 3600 * 24

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

    def get_throttle_key(self, user_id):
        today = datetime.now(tz).date().isoformat()

        return f"throttle:{user_id}:{today}"

    def get_used_count(self, user_id: int) -> int:
        key = self.get_throttle_key(user_id)
        count = redis.get(key)
        return int(count or 0)

    def is_allowed(self, user_id: int) -> bool:
        count = self.get_used_count(user_id)
        return count < settings.DAILY_LIMIT

    def increment_usage_count(self, user_id: int) -> None:
        key = self.get_throttle_key(user_id)
        count = redis.incr(key)

        if count == 1:
            redis.expire(key, self.TTL_SECONDS)

        return count
