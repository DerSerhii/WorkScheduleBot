import logging
import asyncio

import asyncpg

from schedulebot.config import DB_CONNECT_SET, SUPERUSER_ID, LOG_CONFIG, Role
from schedulebot.database.crud import save_to_members


async def create_db():
    logging.basicConfig(**LOG_CONFIG)
    logging.info('Creating databases...')

    conn: asyncpg.Connection = await asyncpg.connect(**DB_CONNECT_SET)

    with open('db.sql', 'r') as sql:
        sql_create_db = sql.read()
    await conn.execute(sql_create_db)

    logging.info('Initial insert data...')

    sql_fill_role = (f"""
        INSERT INTO roles (role) VALUES ($1), ($2), ($3);
        """, Role.SUPERUSER.value, Role.ADMIN.value, Role.EMPLOYEE.value)
    await conn.execute(*sql_fill_role)

    await save_to_members(conn,
                          tg_id=SUPERUSER_ID,
                          member_alias=Role.SUPERUSER.value.capitalize(),
                          role=Role.SUPERUSER.value)
    await conn.close()
    logging.info("The Database and The Start Tables have been created!")


async def create_pool() -> asyncpg.pool.Pool:
    logging.info('Database connection pool created')
    return await asyncpg.create_pool(**DB_CONNECT_SET)


if __name__ == '__main__':
    # Creating the Initial Database and Start Tables
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
