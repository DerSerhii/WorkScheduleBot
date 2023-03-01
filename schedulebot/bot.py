import logging
from aiogram import Bot, Dispatcher, executor

from settings import TELEGRAM_TOKEN, Handler
from schedulebot import handlers


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(handlers.start, commands=[Handler.START.value])
dp.register_message_handler(handlers.client, commands=[Handler.CLIENT.value])
dp.register_message_handler(handlers.moderator, commands=[Handler.MODERATOR.value])
dp.register_message_handler(handlers.superuser, commands=[Handler.SUPERUSER.value])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
