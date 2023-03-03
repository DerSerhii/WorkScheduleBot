import logging

from aiogram import Bot, Dispatcher, executor

from schedulebot import config, handlers


logging.basicConfig(level=logging.INFO)

if not config.TELEGRAM_TOKEN:
    raise ValueError(
        'The Telegram API Token must be initialized in the package'
        f' <{config.BASE_DIR}> in file <.env> as TELEGRAM_TOKEN=...'
    )


def main() -> None:
    bot = Bot(token=config.TELEGRAM_TOKEN)
    dp = Dispatcher(bot)

    handlers.register_start(dp)
    handlers.register_client(dp)
    handlers.register_admin(dp)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
