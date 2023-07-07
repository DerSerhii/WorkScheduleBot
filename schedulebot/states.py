"""
The module represents objects of states.
"""

from aiogram.dispatcher.filters.state import StatesGroup, State


class MemberRegisterState(StatesGroup):
    """
    This object represents the states for an applicant when registering a new member.
    """
    applicant_role_selection = State()
    applicant_role_confirmation = State()
    sending_contact = State()
    wait_acceptance = State()


class MembershipState(StatesGroup):
    """
    This object represents the states of an managers when accepting a new member.
    """
    applicant_consideration = State()
    member_file_selection = State()
    member_file_confirmation = State()
    acceptance_confirmation = State()
    rejection_confirmation = State()
    input_members_alias = State()
    member_alias_confirmation = State()
