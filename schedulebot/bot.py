import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode

from schedulebot import handlers, database, middlewares, filters
from schedulebot.config import TELEGRAM_TOKEN, BASE_DIR, LOG_CONFIG


logging.basicConfig(**LOG_CONFIG)


if not TELEGRAM_TOKEN:
    logging.error("Telegram API Token is missing")
    raise ValueError(
        'The Telegram API Token must be initialized in the package'
        f' <{BASE_DIR}> in file <.env> as TELEGRAM_TOKEN=...'
    )


async def on_startup(dp: Dispatcher) -> None:
    pool = await database.create_pool()
    middlewares.setup(dp, pool)
    filters.setup(dp)
    handlers.setup(dp)
    logging.info('Setup completed.')


async def on_shutdown(dp: Dispatcher) -> None:
    logging.warning('Shutting down...')
    await dp.bot.session.close()
    await dp.storage.reset_all()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bot stopped!')


def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    storage = RedisStorage2('localhost', 6379, db=1) # todo config
    dp = Dispatcher(bot, storage=storage)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
