import redis.asyncio as redis

from django.conf import settings

from aiogram import BaseMiddleware
from datetime import datetime

from zoneinfo import ZoneInfo


class DailyThrottle:
    def __init__(self, redis: redis.Redis, limit=3, seconds=3600 * 24):
        self.redis = redis
        self.limit = limit
        self.seconds = seconds

    def _get_key(self, user_id: int):
        date = datetime.now(ZoneInfo("Asia/Tashkent")).date().isoformat()
        return f"throttle:{user_id}:{date}"

    async def is_allowed(self, user_id: int):
        key = self._get_key(user_id)
        count = await self.redis.get(key)

        return int(count or 0) < self.limit

    async def increment(self, user_id: int) -> None:
        key = self._get_key(user_id)

        new_count = await self.redis.incr(key)

        if new_count == 1:
            self.redis.expire(key, self.seconds)


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self):
        self.limit = settings.DAILY_LIMIT

        self.redis = redis.Redis.from_url(settings.REDIS_URL)

    async def __call__(self, handler, event, data):

        user_id = event.from_user.id

        if await self.is_allowed(user_id):
            return await handler(event, data)

    def _get_key(self, user_id):
        tz = ZoneInfo("Asia/Tashkent")
        today = datetime.now(tz).date().isoformat()

        return f"throttle:{user_id}:{today}"

    async def is_allowed(self, user_id):
        key = self._get_key(user_id)
        count = self.redis.get(key)

        return int(count or 0) < self.limit
