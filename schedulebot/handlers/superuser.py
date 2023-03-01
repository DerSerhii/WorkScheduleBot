from aiogram import types

import schedulebot.message as msg


async def superuser(message: types.Message):
    await message.answer(msg.SUPERUSER)
