import logging
from dataclasses import dataclass
from typing import Iterable, List

from asyncpg import Connection, Record

from ..config import Role


@dataclass
class Staff:
    name: str
    role: str


async def get_staff(db: Connection, *, is_superuser: bool = True) -> List[Staff]:
    staff: List[Record]
    sql = """
        SELECT name, role FROM users
        JOIN roles ON (users.role_id=roles.id)
    """
    if is_superuser:
        sql = sql + 'WHERE role != $1;'
        staff = await db.fetch(sql, Role.SUPERUSER.value)
    else:
        sql = sql + 'WHERE role != $1;'
        staff = await db.fetch(sql, Role.SUPERUSER.value)
    return [Staff(name=rec['name'], role=rec['role']) for rec in staff]
