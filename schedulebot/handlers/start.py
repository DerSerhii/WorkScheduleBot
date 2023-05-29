import logging

import asyncpg
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType

from .. import messages as bot_msg
from ..states import RegisterUserState
from ..keyboards import StartMarkup
from ..config import SUPERUSER_ID, Role
from ..database import save_to_users
from ..filters.test_filter import TestFilter


async def start(message: Message):
    """
    Initial step No.1
    Outputs the first message (greeting) when starting the bot.
    Provides two inline buttons: <admin> and <employee> to choose a role.
    """
    msg_text = bot_msg.START % message.from_user.first_name
    markup = StartMarkup.start()
    await message.answer(text=msg_text, parse_mode='html', reply_markup=markup)
    await RegisterUserState.role.set()


async def confirm_role(call: CallbackQuery, state: FSMContext):
    """
    Initial step No.2
    Confirmation of the user's role.
    """
    await call.message.delete_reply_markup()

    role = call.data
    markup = StartMarkup.confirm_role()
    msg_text = bot_msg.CONFIRM_ROLE % role.capitalize()
    await call.message.answer(text=msg_text, parse_mode='html', reply_markup=markup)
    await state.update_data(role=role, msg_choose_id=call.message.message_id)
    await RegisterUserState.confirm_role.set()


async def back_choose_role(call: CallbackQuery, state: FSMContext) -> None:
    """
    Back to step No.1 — role selection.
    """
    chat_id = call.from_user.id
    data = await state.get_data()
    msg_choose_id = data['msg_choose_id']
    markup = StartMarkup.start()
    await call.message.delete()
    await call.bot.edit_message_reply_markup(chat_id=chat_id,
                                             message_id=msg_choose_id,
                                             reply_markup=markup)
    await RegisterUserState.previous()


async def send_contact_to_verification(call: CallbackQuery, state: FSMContext) -> None:
    """
    Initial step No.3
    Suggests the user to submit a contact for verification.
    """
    await call.message.delete_reply_markup()

    async with state.proxy() as data:
        role = data.get('role')
        data.pop('msg_choose_id')

    if role == Role.ADMIN.value:
        whom = 'них %s' % Role.SUPERUSER.value
    elif role == Role.EMPLOYEE.value:
        whom = 'свого графіку, %s' % Role.ADMIN.value
    else:
        raise ValueError(f'Got an unknown role: {role}')

    name = call.message.chat.first_name
    msg_text = bot_msg.SENT_CONTACT % (name, whom)
    markup = StartMarkup.contact()
    await call.message.answer(text=msg_text, parse_mode='html', reply_markup=markup)
    await RegisterUserState.contact.set()


async def forward_contact_for_confirmation(message: Message, state: FSMContext):
    """
    Initial step No.4
    Forwarding a contact for verification.
    """
    # forward to superuser
    data = await state.get_data()
    user_role = data['role']
    user_id = message.contact.user_id
    user_name = message.contact.full_name
    user_phone = message.contact.phone_number

    # list_users =

    msg_text = bot_msg.NEW_USER_REQUEST % (user_name, user_role)
    await message.forward(SUPERUSER_ID, protect_content=True)
    await message.bot.send_message(chat_id=SUPERUSER_ID,
                                   text=msg_text,
                                   parse_mode='html',
                                   reply_markup=StartMarkup.confirm_user())
    user_data = {
        'user_id': user_id,
        'user_name': user_name,
        'user_role': user_role,
        'user_phone': user_phone
    }
    await state.storage.set_state(chat=SUPERUSER_ID, state='ConfirmUserState:consideration')
    await state.storage.set_data(chat=SUPERUSER_ID, data=user_data)

    # reply to current user
    await message.answer(text=bot_msg.SENT_REQUEST, reply_markup=ReplyKeyboardRemove())
    await RegisterUserState.confirm_user.set()


# for debug
async def test(message: types.Message, middleware, from_filter):
    answer = f'{middleware=} \n{from_filter=}'
    await message.answer(
        answer,
        parse_mode='html',
    )
    return {'from_handler': 'This is data from handler'}


# ***************************************************
# Registration of all functions that explained above
# ***************************************************
def register_start(dp: Dispatcher):
    # Step 1
    dp.register_message_handler(callback=start, commands=['start'])
    # Step 2
    dp.register_callback_query_handler(callback=confirm_role,
                                       state=RegisterUserState.role)
    # Step 3
    dp.register_callback_query_handler(callback=send_contact_to_verification,
                                       text=['confirm_role'],
                                       state=RegisterUserState.confirm_role)
    dp.register_callback_query_handler(back_choose_role,
                                       text=['reject_role'],
                                       state=RegisterUserState.confirm_role)
    # Step 4
    dp.register_message_handler(callback=forward_contact_for_confirmation,
                                content_types=ContentType.CONTACT,
                                state=RegisterUserState.contact)
    # for debug
    # dp.register_message_handler(test, TestFilter(), commands=['test'])
