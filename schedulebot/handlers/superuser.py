from aiogram import types, Dispatcher

import schedulebot.messages as msg


async def start_help(message: types.Message):
    answer_txt = msg.HELP_SUPERUSER % message.from_user.first_name
    await message.answer(
        text=answer_txt,
        parse_mode='html',
    )


def register_superuser(dp: Dispatcher):
    dp.register_message_handler(start_help,
                                is_superuser=True,
                                commands=['start', 'help'])
