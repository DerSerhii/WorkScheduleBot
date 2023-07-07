"""
The module represents handlers for Superuser functionality.
"""

import logging

from aiogram import Dispatcher
from asyncpg import Connection
from aiogram.types import Message, CallbackQuery

from .. import messages as bot_msg
from .. import database
from ..config import Role
from ..keyboards import ButtonText, ManagerMenuMarkup


async def superuser_start_help(message: Message):
    """
    This handler sends the first message to Superuser at the startup.
    Also sends this message when you enter commands: `/start` and `/help`.

    The MAIN MANAGER MENU is provided along with the message.

    :param message: An incoming message with the `/start` or `/help` command from Superuser.
    :type message: :obj:`aiogram.types.Message`.
    :return:
    """
    msg_txt = bot_msg.SUPERUSER_START_HELP % message.from_user.full_name
    await message.answer(msg_txt, 'html', reply_markup=ManagerMenuMarkup.main())


async def provide_staff(message: Message, db: Connection):
    """
    This handler sends a message containing the list of staffs, and STAFF MENU.

    :param message: An incoming message with the text=ButtonText.STAFF.value.
    :type message: :obj:`aiogram.types.Message`.
    :param db: A database session with an established connection to the PostgreSQL server.
    :type db: :obj:`asyncpg.Connection`.
    :return:
    """
    if staff_info := await database.get_basic_staff_info(db):
        msg_text = bot_msg.STAFF_LIST_HEADER
        staff_lst = sorted(staff_info, key=lambda stf: stf.role)
        for staff in staff_lst:
            role = next(rl for rl in Role if rl.value == staff.role)
            badge = bot_msg.__dict__[f'{role.name}_BADGE']
            no_file = bot_msg.NO_FILE if staff.role == Role.EMPLOYEE.value and not staff.file_id else ''
            msg_text += bot_msg.STAFF_LIST_ROW % (badge, staff.member_alias, no_file)
    else:
        msg_text = bot_msg.NO_STAFF_YET

    await message.answer(msg_text, 'html', reply_markup=ManagerMenuMarkup.staff())


async def invite_member(call: CallbackQuery):
    """
    This handler sends an invitation message to be forwarded to the new member.

    :param call: An incoming callback query from the callback button INVITE of the STAFF MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`.
    :return:
    """
    await call.answer()
    await call.message.delete_reply_markup()

    promo_code = str(call.from_user.id)[-5:]
    await call.message.answer(bot_msg.PRE_INVITE, 'html')
    await call.message.answer(bot_msg.INVITE % promo_code, 'html')


# ************************************************************************************************
#                 ^^^ REGISTRATION OF ALL HANDLERS THAT EXPLAINED ABOVE ^^^
# ************************************************************************************************

def register_superuser_handlers(dp: Dispatcher):
    """
    This function registers handlers for the Superuser actions.

    ATTENTION! The order of registration is important!

    :param dp: Current update dispatcher.
    :type dp: :obj:`aiogram.Dispatcher`.
    :return:
    """
    dp.register_message_handler(
        superuser_start_help,
        is_superuser=True,
        commands=['start', 'help']
    )
    dp.register_message_handler(
        provide_staff,
        is_superuser=True,
        text=ButtonText.STAFF.value
    )
    dp.register_callback_query_handler(
        invite_member,
        is_superuser=True,
        text='invite'
    )
    logging.info("Registration of Superuser handlers is completed.")
