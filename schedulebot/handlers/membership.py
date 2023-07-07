"""
The module represents handlers for an acceptance procedure to the membership.
It inclusions handlers for an applicant and handlers for acceptance managers.
"""

import logging
import pickle
from typing import List, Dict

from asyncpg import Connection
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType

from . import helpers
from .. import messages as bot_msg
from .. import database
from ..config import Role, SUPERUSER_ID
from ..filters import FileSelectionMenuAccessFilter
from ..keyboards import MembershipMenuMarkup
from ..states import MemberRegisterState, MembershipState


# ************************************************************************************************
#                                       APPLICANT HANDLERS
# ************************************************************************************************

async def applicants_start(message: Message, state: FSMContext):
    """
    This handler sends the first message (greeting) to unregistered member at the startup.
    And the message containing the MEMBER ROLE SELECTION MENU.

    :param message: An incoming message with the `/start` command from an unregistered user.
    :type message: :obj:`aiogram.types.Message`.
    :param state: Current state in the FSM of the applicant.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :return:
    """
    greeting_msg_text = bot_msg.MEMBERSHIP_START % message.from_user.first_name
    await message.answer(greeting_msg_text, 'html')

    role_msg_text = bot_msg.ROLE_SELECTION
    role_msg_markup = MembershipMenuMarkup.member_role_selection()
    role_message = dict(text=role_msg_text, parse_mode='html', reply_markup=role_msg_markup)
    await message.answer(**role_message)

    set_state = MemberRegisterState.applicant_role_selection
    await state.set_state(set_state)

    rollback_point = pickle.dumps((role_message, set_state)).hex()
    await state.update_data(rollback=rollback_point)


async def confirm_applicant_role(call: CallbackQuery):
    """
    This handler requests confirmation of role selection.
    The previous MEMBER ROLE SELECTION MENU replaces by the CONFIRMATION MENU.

    The handler is only used in FSM after the state:
        * MemberRegisterState:applicant_role_selection.

    :param call: An incoming callback query from one of the callback button
        of the MEMBER ROLE SELECTION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`
    :return:
    """
    applicant_role: str = call.data
    msg_text = bot_msg.CONFIRM_APPLICANT_ROLE % applicant_role.capitalize()
    msg_markup = MembershipMenuMarkup.confirmation(applicant_role)
    await call.message.edit_text(msg_text, 'html', reply_markup=msg_markup)
    await MemberRegisterState.applicant_role_confirmation.set()


async def send_applicant_contact_to_verification(call: CallbackQuery, state: FSMContext):
    """
    This handler provides the CONTACT MENU to send an applicant's contact
    with a phone number for verification.

    The handler is only used in FSM after the state:
        * MemberRegisterState:applicant_role_confirmation.

    :param call: An incoming callback query from the callback button CONFIRM
        of the CONFIRMATION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`.
    :param state: Current state in the FSM of the applicant.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :return:
    """
    await call.message.delete()

    applicant_role: str = call.data.split(':')[-1]
    if applicant_role == Role.ADMIN.value:
        access = bot_msg.ACCESS_ADMIN
    elif applicant_role == Role.EMPLOYEE.value:
        access = bot_msg.ACCESS_EMPLOYEE
    else:
        raise helpers.RoleException(f"Got an invalid role for membership: {applicant_role}")

    msg_text = bot_msg.SEND_CONTACT % access
    msg_markup = MembershipMenuMarkup.send_contact()
    await call.message.answer(msg_text, 'html', reply_markup=msg_markup)

    await state.update_data(role=applicant_role)
    await MemberRegisterState.sending_contact.set()


async def forward_applicant_contact_to_accepting_manager(message: Message,
                                                         state: FSMContext,
                                                         db: Connection):
    """
    This handler forwards an incoming applicant's contact to an accepting manager.
    And sends to an accepting manager the message containing the APPLICANT CONSIDERATION MENU.
    Also notifies the applicant that he needs to wait.

    The handler is only used in FSM after the state:
        * MemberRegisterState:sending_contact.

    :param message: An incoming message containing the applicant's contact (ContentType.CONTACT).
    :type message: :obj:`aiogram.types.Message`.
    :param state: Current state in the FSM of the applicant.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :param db: A database session with an established connection to the PostgreSQL server.
    :type db: :obj:`asyncpg.Connection`.
    :return:
    """
    await message.answer(bot_msg.WAIT_FOR_ANSWER, reply_markup=ReplyKeyboardRemove())
    await MemberRegisterState.wait_acceptance.set()

    state_data = await state.get_data()
    applicant_role: str = helpers.get_and_check_role(state_data)

    applicant_data = {
        'tg_id': message.contact.user_id,
        'tg_name': message.contact.full_name,
        'role': applicant_role,
        'phone': message.contact.phone_number,
    }

    msg_text = bot_msg.MEMBERSHIP_REQUEST % (applicant_data['tg_name'], applicant_role.capitalize())
    is_files = True

    if applicant_role == Role.EMPLOYEE.value:
        free_files = await helpers.find_unreserved_files(db)
        applicant_data.update(free_files=free_files)
        if not free_files:
            msg_text += bot_msg.MISSING_FREE_FILES
            is_files = False

    msg_markup = MembershipMenuMarkup.applicant_consideration(is_files=is_files)
    membership_message = dict(text=msg_text, parse_mode='html', reply_markup=msg_markup)
    await message.forward(SUPERUSER_ID, protect_content=True)
    await message.bot.send_message(SUPERUSER_ID, **membership_message)

    set_state = MembershipState.applicant_consideration
    await state.storage.set_state(chat=SUPERUSER_ID, state=set_state)

    rollback_point = pickle.dumps((membership_message, set_state)).hex()
    applicant_data.update(rollback=rollback_point)
    await state.storage.set_data(chat=SUPERUSER_ID, data=applicant_data)


# ************************************************************************************************
#                                     ACCEPTING MANAGER HANDLERS
# ************************************************************************************************

async def provide_member_file_selection_menu(call: CallbackQuery, state: FSMContext, files: List[Dict]):
    """
    This handler provides the MEMBER FILE SELECTION MENU instead the APPLICANT CONSIDERATION MENU
    if an applicant is Employee, and the Google folder contains free documents
    (files not assigned to other members).
    This check is carried out using the FileSelectionMenuAccessFilter.

    File selection for the applicant automatically means confirmation of his acceptance to membership.

    The handler is only used in the FSM after the state:
        * MembershipState.applicant_consideration.

    :param call: An incoming callback query from the callback button ACCEPT
        of the APPLICANT CONSIDERATION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`
    :param state: Current state in FSM of the accepting manager.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :param files: List of dicts containing data about Document files passed
        from the FileSelectionMenuAccessFilter.
    :type files: :obj:`base.List[base.Dict]`
    :return:
    """
    await call.answer()

    msg_text = bot_msg.MEMBER_FILE_SELECTION
    msg_markup = MembershipMenuMarkup.member_file_selection(files)
    message = dict(text=msg_text, parse_mode='html', reply_markup=msg_markup)
    await call.message.edit_text(**message)

    set_state = MembershipState.member_file_selection
    await state.set_state(set_state)

    rollback_point = pickle.dumps((message, set_state)).hex()
    await state.update_data(rollback=rollback_point)


async def confirm_membership_decision(call: CallbackQuery, state: FSMContext):
    """
    This handler requests confirmation of a membership decision.
    The previous APPLICANT CONSIDERATION MENU or the MEMBER FILE SELECTION MENU
    replaces by the CONFIRMATION MENU.
    It is used for applicants to whom a file from the Google folder will not be pinned.

    The handler is only used in FSM after states:
        * MembershipState.applicant_consideration,
        * MembershipState.member_file_selection.

    :param call: An incoming callback query from the callback buttons ACCEPT_WITHOUT_FILE or REJECT
        of the APPLICANT CONSIDERATION MENU, or the MEMBER FILE SELECTION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`.
    :param state: Current state in FSM of the accepting manager.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :return:
    """
    await call.answer()

    state_data: dict = await state.get_data()
    applicant_role = helpers.get_and_check_role(state_data)

    if call.data == 'accepted':
        if applicant_role == Role.EMPLOYEE.value:
            msg_text = bot_msg.EMPLOYEE_WITHOUT_FILE_ACCEPTANCE_CONFIRMATION
        elif applicant_role == Role.ADMIN.value:
            msg_text = bot_msg.ADMIN_ACCEPTANCE_CONFIRMATION
        else:
            raise helpers.RoleException(f"Got an invalid role for membership: {applicant_role}")
        await MembershipState.acceptance_confirmation.set()

    elif call.data == 'rejected':
        msg_text = bot_msg.MEMBERSHIP_REJECTION_CONFIRMATION
        await MembershipState.rejection_confirmation.set()
    else:
        raise ValueError(f"Got an unknown callback_data: '{call.data}'")

    markup = MembershipMenuMarkup.confirmation(call.data)
    await call.message.edit_text(msg_text, 'html', reply_markup=markup)


async def confirm_choosing_in_member_file_selection_menu(call: CallbackQuery, state: FSMContext):
    """
    This handler requests confirmation of a selected file.
    The previous MEMBER FILE SELECTION MENU replaces by the CONFIRMATION MENU.

    The handler is only used in FSM after state:
        * MembershipState.member_file_selection.

    :param call: An incoming callback query from one of the callback button FILENAME
        of the MEMBER FILE SELECTION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`
    :param state: Current state in FSM of the accepting manager.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :return:
    """
    await call.answer()

    google_file_id: str = call.data
    state_data: dict = await state.get_data()
    free_files_in_google_folder: list[dict] = state_data.get('free_files')

    if file := [doc for doc in free_files_in_google_folder if google_file_id in doc.values()]:
        # Google file id is always unique
        filename = file[0].get('name')
        msg_text = bot_msg.MEMBER_FILE_CONFIRMATION % filename
        markup = MembershipMenuMarkup.confirmation()
        await call.message.edit_text(msg_text, 'html', reply_markup=markup)
        await state.update_data(filename=filename, file_id=google_file_id)
        await MembershipState.member_file_confirmation.set()
    else:
        ValueError(f"Got an unknown Google file id: {google_file_id}")


async def request_members_alias(call: CallbackQuery, state: FSMContext):
    """
    This handler performs an alias request for a new member.

    The handler is only used in FSM after the states:
        * MembershipState:acceptance_confirmation,
        * MembershipState:member_file_confirmation.

    :param call: An incoming callback query from the callback button CONFIRM of the CONFIRMATION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`.
    :param state: Current state in the FSM of the accepting manager.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :return:
    """
    await call.answer()

    async with state.proxy() as data:
        member_name = data.pop('filename', data['tg_name'])
        data.pop('free_files')

    msg_text = bot_msg.ASKING_MEMBERS_ALIAS % (member_name + ' ' + data['role'].capitalize())
    message = dict(text=msg_text, parse_mode='html')
    await call.message.edit_text(**message)

    set_state = MembershipState.input_members_alias
    await state.set_state(set_state)

    rollback_point = pickle.dumps((message, set_state)).hex()
    await state.update_data(rollback=rollback_point)


async def confirm_members_alias(message: Message, state: FSMContext):
    """
    This handler requests confirmation of a member's alias.

    The handler is only used in FSM after states:
        * MembershipState:input_members_alias.

    :param message: An incoming message containing member's alias.
    :type message: :obj:`aiogram.types.Message`.
    :param state: Current state in FSM of the accepting manager.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :return:
    """
    await message.delete()
    await message.bot.delete_message(message.chat.id, message.message_id - 1)

    member_alias = message.text
    msg_text = bot_msg.ALIAS_CONFIRMATION % member_alias
    markup = MembershipMenuMarkup.confirmation()
    await message.answer(msg_text, 'html', reply_markup=markup)

    await state.update_data(member_alias=member_alias)
    await MembershipState.member_alias_confirmation.set()


async def finish_acceptance_to_membership(call: CallbackQuery, state: FSMContext, db: Connection):
    """
    This handler adds an applicant to database.
    If the applicant has been rejected, he will be added to the `blacklist` table.
    If the applicant has been accepted, he will be added to the `members` table.

    The applicant and acceptance managers are notified of the result.

    The handler is only used in the FSM after the states:
        * MembershipState:rejection_confirmation,
        * MembershipState.member_alias_confirmation.

    FSM states for an applicant, and a current acceptance manager ends here.

    :param call: An incoming callback query from the callback button CONFIRM of the CONFIRMATION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`.
    :param state: Current state in the FSM of the accepting manager.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :param db: A database session with an established connection to the PostgreSQL server.
    :type db: :obj:`asyncpg.Connection`.
    :return:
    """
    await call.answer()
    await call.message.delete()

    state_data: dict = await state.get_data()

    if member_alias := state_data.get('member_alias'):
        save_to_db = database.save_to_members
        role = next(rl for rl in Role if rl.value == state_data['role'])
        badge = bot_msg.__dict__[f'{role.name}_BADGE']
        notify_msg_text = bot_msg.ADDED_TO_MEMBERS % (badge, member_alias, role.value.capitalize())
        answer_msg_text = bot_msg.ACCESS_ALLOWED % role.value.capitalize()
        sticker = bot_msg.STICKER_CONGRATULATION
    else:
        save_to_db = database.save_to_blacklist
        notify_msg_text = bot_msg.ADDED_TO_BLACK_LIST % (state_data['tg_name'], state_data['phone'])
        answer_msg_text = bot_msg.ACCESS_DENIED
        sticker = bot_msg.STICKER_REGRET

    await save_to_db(db, **state_data)

    await state.finish()
    await state.storage.finish(user=state_data['tg_id'])

    await call.message.answer(notify_msg_text, 'html')
    await call.bot.send_message(state_data['tg_id'], answer_msg_text)
    await call.bot.send_sticker(state_data['tg_id'], sticker)


# ************************************************************************************************
#                                        COMMON HANDLERS
# ************************************************************************************************

async def rollback_to_menu_if_choosing_mistake(call: CallbackQuery, state: FSMContext):
    """
    This handler rolls back to a previous menu if any user decided that he made a mistake in the choice.

    The handler is used for all states of a current user.

    :param call: An incoming callback query from the callback button BACK of the CONFIRMATION MENU.
    :type call: :obj:`aiogram.types.CallbackQuery`.
    :param state: Current state in FSM for any user.
    :type state: :obj:`aiogram.dispatcher.FSMContext`.
    :return:
    """
    await call.answer()

    state_data = await state.get_data()
    rollback_point = bytes.fromhex(state_data['rollback'])
    message, set_state = pickle.loads(rollback_point)

    await call.message.edit_text(**message)
    await state.set_state(set_state)


# ************************************************************************************************
#                 ^^^ REGISTRATION OF ALL HANDLERS THAT EXPLAINED ABOVE ^^^
# ************************************************************************************************

def register_membership_handlers(dp: Dispatcher):
    """
    This function registers handlers for the membership procedure.

    ATTENTION! The order of registration is important!

    :param dp: Current update dispatcher.
    :type dp: :obj:`aiogram.Dispatcher`.
    :return:
    """
    dp.register_message_handler(
        applicants_start,
        commands='start'
    )
    dp.register_callback_query_handler(
        rollback_to_menu_if_choosing_mistake,
        state='*',
        text='back'
    )
    dp.register_callback_query_handler(
        confirm_applicant_role,
        state=MemberRegisterState.applicant_role_selection
    )
    dp.register_callback_query_handler(
        send_applicant_contact_to_verification,
        state=MemberRegisterState.applicant_role_confirmation,
        text_contains='confirm'
    )
    dp.register_message_handler(
        forward_applicant_contact_to_accepting_manager,
        state=MemberRegisterState.sending_contact,
        content_types=ContentType.CONTACT
    )
    dp.register_callback_query_handler(
        provide_member_file_selection_menu,
        FileSelectionMenuAccessFilter(),
        state=MembershipState.applicant_consideration,
        text='accepted'
    )
    dp.register_callback_query_handler(
        confirm_membership_decision,
        state=[MembershipState.applicant_consideration,
               MembershipState.member_file_selection],
        text=['accepted', 'rejected']
    )
    dp.register_callback_query_handler(
        confirm_choosing_in_member_file_selection_menu,
        state=MembershipState.member_file_selection
    )
    dp.register_callback_query_handler(
        request_members_alias,
        state=[MembershipState.acceptance_confirmation,
               MembershipState.member_file_confirmation],
        text_contains='confirmed'
    )
    dp.register_message_handler(
        confirm_members_alias,
        state=MembershipState.input_members_alias
    )
    dp.register_callback_query_handler(
        finish_acceptance_to_membership,
        state=[MembershipState.rejection_confirmation,
               MembershipState.member_alias_confirmation],
        text_contains='confirmed'
    )
    logging.info("Registration of Membership handlers is completed.")
