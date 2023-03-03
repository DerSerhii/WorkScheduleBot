import logging
from aiogram import Bot, Dispatcher, executor

from settings import TELEGRAM_TOKEN
from schedulebot import handlers


logging.basicConfig(level=logging.INFO)


def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(bot)

    handlers.register_start(dp)
    handlers.register_client(dp)
    handlers.register_admin(dp)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
