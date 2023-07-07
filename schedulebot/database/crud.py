"""
The module implements the functions of interaction between the bot and the database.
"""

import logging

from asyncpg import Connection, Record
from typing import Union, Optional, List, AnyStr

from schedulebot.config import Role
from schedulebot.models import Staff


async def save_to_members(db_conn: Connection, *,
                          tg_id: Union[int, str],
                          member_alias: str,
                          role: str,
                          phone: Union[int, str, None] = None,
                          file_id: Optional[str] = None,
                          **kwargs):
    """
    Records a member to the database table `members`.

    :param db_conn: A database session with an established connection to the PostgreSQL server.
    :type db_conn: :obj:`asyncpg.Connection`.
    :param tg_id: Member’s Telegram ID.
    :type tg_id: :obj:`typing.Union[int, str]`.
    :param member_alias: Custom member's username.
    :type member_alias: :obj:`str`.
    :param role: Member role.
    :type role: :obj:`str`.
    :param phone: Member’s phone number.
    :type phone: :obj:`typing.Union[int, str, None]`.
    :param file_id: The Google Document ID associated with this user.
    :type file_id: :obj:`typing.Union[str, None]`.
    :param kwargs: Necessary when receiving unwanted arguments.
    :return:
    """
    if isinstance(tg_id, str):
        tg_id = int(tg_id)
    if isinstance(phone, int):
        tg_id = str(phone)

    sql_query = (
        """
        INSERT INTO members (tg_id, member_alias, role_id, phone, file_id) VALUES (
            ($1), ($2), (SELECT id FROM roles WHERE role=($3)), ($4), ($5)
        );
        """, tg_id, member_alias, role, phone, file_id
    )
    await db_conn.execute(*sql_query)
    logging.info(f"<{member_alias}> added to members")


async def save_to_blacklist(db_conn: Connection, *,
                            tg_id: Union[int, str],
                            tg_name: str,
                            phone: Union[int, str],
                            **kwargs):
    """
    Records a member to the database table `blacklist`.

    :param db_conn: A database session with an established connection to the PostgreSQL server.
    :type db_conn: :obj:`asyncpg.Connection`.
    :param tg_id: Member’s Telegram ID.
    :type tg_id: :obj:`typing.Union[int, str]`.
    :param tg_name: Member’s Telegram Username.
    :type tg_name: :obj:`str`.
    :param phone: Member’s phone number.
    :type phone: :obj:`typing.Union[int, str]`.
    :param kwargs: Necessary when receiving unwanted arguments.
    :return:
    """
    if isinstance(tg_id, str):
        tg_id = int(tg_id)
    if isinstance(phone, int):
        tg_id = str(phone)

    sql_query = (
        f"""
        INSERT INTO blacklist (tg_id, name, phone) VALUES (
            ($1), ($2), ($3)
        );
        """, tg_id, tg_name, phone
    )
    await db_conn.execute(*sql_query)
    logging.info(f"<{tg_name}> added to blacklist")


async def get_file_ids(db_conn: Connection) -> List[str]:
    """
    Retrieves all Google Document IDs associated with members from the database.

    :param db_conn: A database session with an established connection to the PostgreSQL server.
    :type db_conn: :obj:`asyncpg.Connection`.
    :return: A list of Google Document IDs or an empty list if there are none.
    :rtype: :obj:`typing.List[str]`
    """
    sql_query = """
        SELECT file_id FROM members WHERE file_id IS NOT NULL;
        """
    files: List[Record] = await db_conn.fetch(sql_query)
    return [record['file_id'] for record in files]


async def get_basic_staff_info(db: Connection) -> List[Staff]:
    """
    Retrieves a basic staff's information from the database,
    such us `tg_id`, `member_alias`, `role`, `file_id`
    and returns it as Staff objects.

    :param db: A database session with an established connection to the PostgreSQL server.
    :type db: :obj:`asyncpg.Connection`.
    :return: A list of Staff objects with a basic info.
    :rtype: :obj:`typing.List[schedulebot.models.Staff]`.
    """
    sql_query = """
        SELECT tg_id, member_alias, role, file_id FROM members
        JOIN roles ON (members.role_id=roles.id)
        WHERE role != $1
        ORDER BY members.member_alias ASC;
    """
    staff_info: List[Record] = await db.fetch(sql_query, Role.SUPERUSER.value)
    return [Staff(**record) for record in staff_info]
