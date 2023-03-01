import logging
from aiogram import Bot, Dispatcher, executor

from settings import TELEGRAM_TOKEN, Handler
from schedulebot import handlers


COMMAND_HANDLERS = {
    Handler.START.value: handlers.start,
    Handler.CLIENT.value: handlers.client,
    Handler.MODERATOR.value: handlers.moderator,
    Handler.SUPERUSER.value: handlers.superuser,
}


logging.basicConfig(level=logging.INFO)


def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(bot)

    for command, handler in COMMAND_HANDLERS.items():
        dp.register_message_handler(handler, commands=[command])

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
