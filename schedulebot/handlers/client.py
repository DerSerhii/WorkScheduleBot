from aiogram import types

import schedulebot.message as msg


async def client(message: types.Message):
    await message.answer(msg.CLIENT)
