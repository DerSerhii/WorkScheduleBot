import asyncio
import logging

import asyncpg

from schedulebot.config import DB_CONNECT, SUPERUSER_ID, LOG_CONFIG, Role


logging.basicConfig(**LOG_CONFIG)


async def create_db():
    logging.info('Creating databases...')
    con: asyncpg.Connection = await asyncpg.connect(**DB_CONNECT)

    cmd_create_db = open('db.sql', 'r').read()
    await con.execute(cmd_create_db)

    logging.info('Initial insert data...')
    superuser = Role.SUPERUSER.value
    admin = Role.ADMIN.value
    employee = Role.EMPLOYEE.value

    cmd_fill_role = (
        f"""
        INSERT INTO roles (role) VALUES
            ($1),
            ($2),
            ($3);
        """, superuser, admin, employee
    )
    cmd_init_superuser = (
        f"""
        INSERT INTO users (tg_id, name, role_id) VALUES (
            ($1), 
            ($2), 
            (SELECT id FROM roles WHERE role=($3))
        );
        """, SUPERUSER_ID, superuser, superuser
    )
    await con.execute(*cmd_fill_role)
    await con.execute(*cmd_init_superuser)

    await con.close()
    logging.info("The database and start tables have been created!")


async def create_pool():
    logging.info('Database connection pool created')
    return await asyncpg.create_pool(**DB_CONNECT)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
