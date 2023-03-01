import logging
from aiogram import Bot, Dispatcher, executor

import settings
from schedulebot import handlers


logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(handlers.start, commands=['start'])
dp.register_message_handler(handlers.client, commands=['client'])
dp.register_message_handler(handlers.moderator, commands=['moderator'])
dp.register_message_handler(handlers.superuser, commands=['superuser'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
