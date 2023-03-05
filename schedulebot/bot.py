import logging

from aiogram import Bot, Dispatcher, executor

from schedulebot import handlers, database
from schedulebot.config import TELEGRAM_TOKEN, BASE_DIR, LOG_CONFIG


logging.basicConfig(**LOG_CONFIG)


if not TELEGRAM_TOKEN:
    logging.error("Telegram API Token is missing")
    raise ValueError(
        'The Telegram API Token must be initialized in the package'
        f' <{BASE_DIR}> in file <.env> as TELEGRAM_TOKEN=...'
    )


async def on_startup(dp: Dispatcher):
    pool = await database.create_pool()

    handlers.register_start(dp)
    handlers.register_employee(dp)
    handlers.register_admin(dp)


async def on_shutdown(dp: Dispatcher):
    logging.warning('Shutting down...')
    await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bot stopped!')


def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(bot)

    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
