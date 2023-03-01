from aiogram import types

import schedulebot.message as msg


async def start(message: types.Message):
    name = message.chat.first_name
    name = name if name else '👤'
    await message.answer(msg.START % name)
