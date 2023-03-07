import asyncpg
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware, BaseMiddleware
from aiogram.types.base import TelegramObject


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['update']

    def __init__(self, pool):
        super().__init__()
        self.pool: asyncpg.pool.Pool = pool

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        data['db'] = self.pool

    async def post_process(self, obj: TelegramObject, data: dict, *args):
        if db := data.get('db', None):
            await db.close()
