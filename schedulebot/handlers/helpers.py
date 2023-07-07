"""
Module provides helper functions for handlers.
"""

from typing import List, Dict

from aiogram.types import CallbackQuery

from .. import messages as bot_msg
from .. import database
from .. import googledrive
from ..config import Role


class RoleException(ValueError):
    """ This object represents a custom role exception."""
    pass


def get_and_check_role(data: Dict) -> str:
    """
    Returns a value of the user's role from the passed state data dictionary.

    If the role item is absent in the dictionary, or the role value is unknown
    will raise exception.

    :param data: A passed state data.
    :type data: :obj:`typing.Dict`.
    :return: A value of the user's role.
    :rtype: :obj:`str`
    """
    role: str = data.get('role')

    if not role:
        raise RoleException("Key 'role' in state data is absent.")
    elif not any(item.value == role for item in Role):
        raise RoleException(f"Got an unknown role: {role}")
    else:
        return role


async def find_unreserved_files(db_conn) -> List[Dict]:
    """
    Looks for unreserved files (documents) in Google working folder.
    :param db_conn: A database session with an established connection to the PostgreSQL server.
    :type db_conn: :obj:`asyncpg.Connection`.
    :return: A list of dict with data of Google files (documents) or an empty list if there are none.
    :rtype: :obj:`typing.List[typing.Dict]`
    """
    lst_files_google = await googledrive.get_list_files()
    lst_id_docs_in_db = await database.get_file_ids(db_conn)
    return [file for file in lst_files_google if file['id'] not in lst_id_docs_in_db]


async def notify_application_results(call: CallbackQuery, state_data: Dict):
    """
    This function sends notifications to the applicant and acceptance managers
    about the application results.

    :param call: Passed an incoming callback query from the place where the function was called.
    :type call: :obj:`aiogram.types.CallbackQuery`.
    :param state_data: Passed current state data from the place where the function was called.
    :type state_data: :obj:`base.Dict`.
    :return:
    """
    if member_alias := state_data.get('member_alias'):
        role = next(rl for rl in Role if rl.value == state_data['role'])
        badge = bot_msg.__dict__[f'{role.name}_BADGE']
        notify_msg_text = bot_msg.ADDED_TO_MEMBERS % (badge, member_alias, role.value.capitalize())
        answer_msg_text = bot_msg.ACCESS_ALLOWED % role.value.capitalize()
        sticker = bot_msg.STICKER_CONGRATULATION
    else:
        notify_msg_text = bot_msg.ADDED_TO_BLACK_LIST % (state_data['tg_name'], state_data['phone'])
        answer_msg_text = bot_msg.ACCESS_DENIED
        sticker = bot_msg.STICKER_REGRET

    await call.message.answer(notify_msg_text, 'html')
    await call.bot.send_message(state_data['tg_id'], answer_msg_text)
    await call.bot.send_sticker(state_data['tg_id'], sticker)
