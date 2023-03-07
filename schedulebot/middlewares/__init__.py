import asyncpg
from aiogram import Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# from .data import DataMiddleware
from .db_middleware import  DatabaseMiddleware
from .test_middleware import TestMiddleware


def setup(dp: Dispatcher, pool: asyncpg.pool.Pool, config: dict = None):
    environment_data = {
        "config": config,
    }
    # dp.setup_middleware(LoggingMiddleware())
    # dp.setup_middleware(EnvironmentMiddleware(context=environment_data))
    dp.setup_middleware(DatabaseMiddleware(pool))
    # dp.setup_middleware(DataMiddleware())
    dp.setup_middleware(TestMiddleware())
