import asyncio
import logging

import asyncpg

from schedulebot.config import DB_CONNECT, SUPERUSER_ID, LOG_CONFIG, Role
from schedulebot.database.crud import save_to_users


async def create_db():
    logging.basicConfig(**LOG_CONFIG)
    logging.info('Creating databases...')

    conn: asyncpg.Connection = await asyncpg.connect(**DB_CONNECT)

    with open('db.sql', 'r') as sql:
        sql_create_db = sql.read()
    await conn.execute(sql_create_db)

    logging.info('Initial insert data...')

    sql_fill_role = (f"""
        INSERT INTO roles (role) VALUES ($1), ($2), ($3);
        """, Role.SUPERUSER.value, Role.ADMIN.value, Role.EMPLOYEE.value)
    await conn.execute(*sql_fill_role)

    await save_to_users(conn,
                        user_id=SUPERUSER_ID,
                        user_name=Role.SUPERUSER.value.capitalize(),
                        user_role=Role.SUPERUSER.value)
    await conn.close()
    logging.info("The Database and The Start Tables have been created!")


async def create_pool() -> asyncpg.pool.Pool:
    logging.info('Database connection pool created')
    return await asyncpg.create_pool(**DB_CONNECT)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
