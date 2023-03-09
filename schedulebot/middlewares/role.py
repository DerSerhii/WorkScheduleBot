import logging

import asyncpg
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware, BaseMiddleware
from aiogram.types import Update
from aiogram.types.base import TelegramObject

from ..config import Role


class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['update']

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        db: asyncpg.pool.Pool = data['db']

        get_role_sql = '''
            SELECT role FROM users 
            INNER JOIN roles ON (users.role_id=roles.id) 
            WHERE tg_id=($1);
        '''

        logging.info(obj)
        user_id = obj['from']['id']
        role_str = await db.fetchval(get_role_sql, user_id)
        data['role'] = Role(role_str)

    async def post_process(self, obj: TelegramObject, data: dict, *args):
        del data['role']
