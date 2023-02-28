import logging
from aiogram import Bot, Dispatcher, executor, types

import settings
import message as msg


logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    name = message.chat.first_name
    name = name if name else '👤'
    await message.answer(msg.START % name)


@dp.message_handler(commands=['client'])
async def client(message: types.Message):
    await message.answer(msg.CLIENT)


@dp.message_handler(commands=['moderator'])
async def moderator(message: types.Message):
    await message.answer(msg.MODERATOR)


@dp.message_handler(commands=['superuser'])
async def superuser(message: types.Message):
    await message.answer(msg.SUPERUSER)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

