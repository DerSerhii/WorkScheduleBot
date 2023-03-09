import asyncpg
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject


class DatabaseMiddleware(LifetimeControllerMiddleware):

    def __init__(self, pool):
        super().__init__()
        self.pool: asyncpg.pool.Pool = pool

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        data['db'] = await self.pool.acquire()
        data['pool'] = self.pool

    async def post_process(self, obj, data, *args):
        if db := data.get("db"):
            await self.pool.release(db)
