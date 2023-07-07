import logging
from typing import Optional, Union, Collection

from aiogram import Dispatcher
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from aiogram.types.base import TelegramObject

from ..config import Role


class RoleFilter(BoundFilter):
    key = 'role'

    def __init__(
            self,
            role: Union[None, Role, Collection[Role]] = None,
    ):
        if role is None:
            self.roles = None
        elif isinstance(role, Role):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def check(self, obj: TelegramObject):
        if self.roles is None:
            return True
        data = ctx_data.get()
        return data.get("role") in self.roles


class SuperuserFilter(BoundFilter):
    key = 'is_superuser'

    def __init__(self, is_superuser: Optional[bool] = None):
        self.is_superuser = is_superuser

    async def check(self, obj: TelegramObject):
        if self.is_superuser is None:
            return True
        data = ctx_data.get()

        return (data.get("role") is Role.SUPERUSER) == self.is_superuser


class FileSelectionMenuAccessFilter(BoundFilter):

    async def check(self, call: CallbackQuery):
        state = Dispatcher.get_current().current_state()
        state_data = await state.get_data()
        applicant_role = state_data.get('role')
        free_files_in_google_folder = state_data.get('free_files')
        if applicant_role == Role.EMPLOYEE.value and free_files_in_google_folder:
            return {'files': free_files_in_google_folder}
