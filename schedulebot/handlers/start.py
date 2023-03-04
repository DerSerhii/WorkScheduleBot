from aiogram import types, Dispatcher

import schedulebot.message as msg
import schedulebot.handlers.keyboards as kb


async def start(message: types.Message):
    await message.answer(
        msg.START % message.chat.first_name,
        parse_mode='html',
        reply_markup=kb.mkp_start
    )


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
