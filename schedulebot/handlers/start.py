from aiogram import types, Dispatcher

import schedulebot.messages as msg
import schedulebot.handlers.keyboards as kb
from ..config import Role
from ..filters.test_filter import TestFilter


async def start(message: types.Message):
    answer_txt = msg.START % message.from_user.first_name
    await message.answer(
        text=answer_txt,
        parse_mode='html',
        reply_markup=kb.mkp_start
    )


async def test(message: types.Message, middleware, from_filter):
    answer = f'{middleware=} \n{from_filter=}'
    await message.answer(
        answer,
        parse_mode='html',
    )
    return {'from_handler': 'This is data from handler'}


def register_start(dp: Dispatcher):
    dp.register_message_handler(start,
                                commands=['start'])
    dp.register_message_handler(test,
                                TestFilter(),
                                commands=['test'])
