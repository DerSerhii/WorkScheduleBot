from aiogram import types, Dispatcher

import schedulebot.messages as msg


async def help_superuser(message: types.Message):
    answer_txt = msg.HELP_SUPERUSER % message.from_user.first_name
    await message.answer(
        text=answer_txt,
        parse_mode='html',
    )


def register_superuser(dp: Dispatcher):
    dp.register_message_handler(help_superuser,
                                commands=['help'])


