import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject

from ..config import Role


class RoleFilter(BoundFilter):
    key = 'role'

    def __init__(
            self,
            role: typing.Union[None, Role, typing.Collection[Role]] = None,
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

    def __init__(self, is_superuser: typing.Optional[bool] = None):
        self.is_superuser = is_superuser

    async def check(self, obj: TelegramObject):
        if self.is_superuser is None:
            return True
        data = ctx_data.get()

        return (data.get("role") is Role.SUPERUSER) == self.is_superuser
