import logging
from typing import List
from collections import namedtuple

import asyncpg
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineQuery, InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineQueryResultArticle, InputTextMessageContent

from ..config import Role
from ..database.crud import save_to_blacklist
from ..messages import MSG_HELP_SUPERUSER, PRE_INVITE, INVITE, ASK_NAME, INSERT_TO_USERS, \
    CONGRATULATION, \
    STICKER_CONGRATULATION, REPEAT_NAME_USER, ACKNOWLEDGMENT_USERNAME, REGRET, INSERT_TO_BLACKLIST, \
    STICKER_REGRET
from ..actions.staff import Staff
from ..keyboards import SuperuserMarkup, Button, StartMarkup
from ..actions import get_staff
from ..states import ConfirmUserState
from ..database import save_to_users


# ************************************************************
#                    THE SUPERUSER HANDLERS
# ************************************************************

async def start_help(message: Message):
    answer_txt = MSG_HELP_SUPERUSER % message.from_user.first_name
    markup = SuperuserMarkup.main()
    await message.answer(
        text=answer_txt,
        parse_mode='html',
        reply_markup=markup
    )


async def staff(message: Message, db: asyncpg.Connection):
    staff_: List[Staff] = await get_staff(db)
    text = staff_text(staff_)
    markup = SuperuserMarkup.invite(is_exist=bool(len(staff_)))
    await message.answer(text=text,
                         reply_markup=markup)


# async def invite(call: CallbackQuery):
#     await call.answer(cache_time=20)
#     await call.message.answer(text=PRE_INVITE, parse_mode='html')
#     await call.message.answer(text=INVITE)


async def consideration_new_user(call: CallbackQuery, state: FSMContext,
                                 db: asyncpg.Connection):
    """

    """
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)

    if call.data == 'confirm_user':
        data_user = await state.get_data()
        user_name = data_user['user_name']
        user_role = data_user['user_role']
        if user_role == Role.EMPLOYEE.value:
            list_documents = []
            # if list_documents:

        else:
            msg = ASK_NAME % (user_name, 'Адміністратор')
            await call.message.answer(text=msg, parse_mode='html')
            await ConfirmUserState.name.set()

    else:
        await finite_step_register_user(db, state, call, blacklist=True)


async def acknowledgment_username(message: Message, state: FSMContext):
    """
    Acknowledgment username for the new user.
    Adding a username to the state data.
    """
    user_name = message.text
    msg = ACKNOWLEDGMENT_USERNAME % user_name
    markup = StartMarkup.acknowledgment_name()
    await message.answer(text=msg, parse_mode='html', reply_markup=markup)
    await state.update_data(user_name=user_name)
    await ConfirmUserState.acknowledgment_name.set()


async def acceptance_new_user(call: CallbackQuery,
                              state: FSMContext,
                              db: asyncpg.Connection):
    """
    Initial step No.5 to acceptance a new user when name correct.
    Finishing FSM states for a New User and the Superuser.
    See the module <start.py> for the previous four steps.
    """
    await call.answer()
    await call.message.delete()

    if call.data == 'OK':
        await finite_step_register_user(db, state, call)
    else:
        await call.message.answer(REPEAT_NAME_USER)
        await ConfirmUserState.previous()


async def inline_handler(query: InlineQuery):
    # Створення вікна підтвердження
    confirm_keyboard = InlineKeyboardMarkup(row_width=2)
    confirm_keyboard.add(
        InlineKeyboardButton("OK", callback_data="confirm_ok"),
        InlineKeyboardButton("CANCEL", callback_data="confirm_cancel")
    )

    await query.answer(
        results=[InlineQueryResultArticle(
            id="confirm_window",
            title="Confirm Window",
            input_message_content=InputTextMessageContent(
                message_text="Ви впевнені?",
            ),
            reply_markup=confirm_keyboard
        )],
        cache_time=0
    )


async def confirm_callback_handler(callback_query: CallbackQuery):
    if callback_query.data == "confirm_ok":
        await callback_query.answer("Ви натиснули OK.")
        # Тут ви можете виконати дії, які пов'язані з підтвердженням
    elif callback_query.data == "confirm_cancel":
        await callback_query.answer("Ви натиснули CANCEL.")
        # Тут ви можете виконати дії, які пов'язані з скасуванням

async def test_command(message: Message):
    # Створення inline кнопки з посиланням на бота
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(InlineKeyboardButton("Confirm", callback_data='Test'))

    # Відправлення повідомлення з inline кнопкою
    await message.reply("Натисніть кнопку 'Confirm':", reply_markup=inline_keyboard)


# ************************************************************
# ^^^ REGISTRATION OF ALL HANDLERS THAT EXPLAINED ABOVE ^^^
# ************************************************************

def register_handlers_superuser(dp: Dispatcher):
    dp.register_inline_handler(inline_handler)
    dp.register_message_handler(test_command, text='Test')
    dp.register_message_handler(callback=start_help,
                                is_superuser=True,
                                commands=['start', 'help'])
    dp.register_message_handler(callback=staff,
                                is_superuser=True,
                                text=Button.STAFF.value)
    # dp.register_callback_query_handler(invite,
    #                                    text=['invite'])
    dp.register_callback_query_handler(callback=consideration_new_user,
                                       state=ConfirmUserState.consideration)
    dp.register_message_handler(callback=acknowledgment_username,
                                state=ConfirmUserState.name)
    dp.register_callback_query_handler(callback=acceptance_new_user,
                                       state=ConfirmUserState.acknowledgment_name)
    dp.register_callback_query_handler(lambda c: c.data in ["confirm_ok", "confirm_cancel"])


# ************************************************************
#                 HELPER FUNCTIONS FOR HANDLERS
# ************************************************************

async def finite_step_register_user(db: asyncpg.Connection,
                                    state: FSMContext,
                                    call: CallbackQuery,
                                    *,
                                    blacklist: bool = False):
    """
    The function implements the last step in processing a request to join a new user.

    If the parameter `blacklist=True` then the contact will be added to the database
    in the blacklist table, after which access will be denied to him.

    FSM states for New user and Superuser ends here.
    They are sent messages about the result.
    """
    data_user: dict = await state.get_data()

    if not blacklist:
        save_to_db = save_to_users
        msg_insert = INSERT_TO_USERS
        msg_cong = CONGRATULATION
        sticker = STICKER_CONGRATULATION
    else:
        save_to_db = save_to_blacklist
        msg_insert = INSERT_TO_BLACKLIST
        msg_cong = REGRET
        sticker = STICKER_REGRET

    await save_to_db(db_conn=db, **data_user)

    # sent to superuser
    msg_su = msg_insert % data_user['user_name']
    await call.message.answer(text=msg_su, parse_mode='html')
    await state.finish()

    # sent to new user
    user_id = data_user['user_id']
    await call.bot.send_message(user_id, msg_cong)
    await call.bot.send_sticker(user_id, sticker)
    await state.storage.finish(user=user_id)
