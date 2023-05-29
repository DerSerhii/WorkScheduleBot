from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterUserState(StatesGroup):
    role = State()
    confirm_role = State()
    contact = State()
    confirm_user = State()


class ConfirmUserState(StatesGroup):
    consideration = State()
    name = State()
    acknowledgment_name = State()
