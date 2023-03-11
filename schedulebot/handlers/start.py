import logging

from aiogram import types, Dispatcher
from aiogram.types import Message, CallbackQuery

import schedulebot.messages as msg
from ..keyboards import StartMarkup
from ..config import Role
from ..filters.test_filter import TestFilter


async def start(message: Message):
    answer_txt = msg.START % message.from_user.first_name
    markup = StartMarkup.start()
    await message.answer(
        text=answer_txt,
        parse_mode='html',
        reply_markup=markup
    )


async def confirm_role(call: CallbackQuery):
    await call.answer(cache_time=20)
    name = call.message.chat.first_name
    whom = 'керівнику' if call.data == 'admin' else 'адміністратору'
    markup = StartMarkup.confirm()
    await call.message.answer(
        msg.CONFIRM_ROLE % (name, whom),
        reply_markup=markup
    )


async def test(message: types.Message, middleware, from_filter):
    answer = f'{middleware=} \n{from_filter=}'
    await message.answer(
        answer,
        parse_mode='html',
    )
    return {'from_handler': 'This is data from handler'}


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(confirm_role, text=['admin', 'employee'])
    dp.register_message_handler(test, TestFilter(), commands=['test'])

