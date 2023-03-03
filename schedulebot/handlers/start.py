from aiogram import types, Dispatcher

import schedulebot.message as msg
import schedulebot.handlers.keyboards as kb


async def start(message: types.Message):
    name = message.chat.first_name
    name = name if name else '👤'
    await message.answer(msg.START % name,
                         parse_mode='html',
                         reply_markup=kb.mkp_start
                         )


def register_start(dp: Dispatcher):
    dp.register_message_handler(start,
                                commands=['start']
                                )
