from aiogram import types, Dispatcher

import schedulebot.messages as msg
from ..keyboards import SuperuserMarkup


async def start_help(message: types.Message):
    answer_txt = msg.HELP_SUPERUSER % message.from_user.first_name
    markup = SuperuserMarkup.main()
    await message.answer(
        text=answer_txt,
        parse_mode='html',
        reply_markup=markup
    )


def register_superuser(dp: Dispatcher):
    dp.register_message_handler(start_help,
                                is_superuser=True,
                                commands=['start', 'help'])
