from aiogram import types

import schedulebot.message as msg


async def moderator(message: types.Message):
    await message.answer(msg.MODERATOR)
