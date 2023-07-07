from aiogram import types, Dispatcher

from ..filters.test_filter import TestFilter


async def test(message: types.Message, middleware, from_filter):
    answer = f'{middleware=} \n{from_filter=}'
    await message.answer(
        answer,
        parse_mode='html',
    )
    return {'from_handler': 'This is data from handler'}


# ************************************************************
# ^^^ REGISTRATION OF ALL HANDLERS THAT EXPLAINED ABOVE ^^^
# ************************************************************

def register_debug(dp: Dispatcher):
    dp.register_message_handler(test, TestFilter(), commands=['test'])
