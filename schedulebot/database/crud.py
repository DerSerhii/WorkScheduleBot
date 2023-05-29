import asyncpg


async def save_to_users(db_conn: asyncpg.Connection,
                        *,
                        user_id: int,
                        user_name: str,
                        user_role: str,
                        user_phone: str = None,
                        user_document: str = None):
    sql = (
        f"""
        INSERT INTO users (tg_id, name, role_id, phone, document) VALUES (
            ($1), ($2), (SELECT id FROM roles WHERE role=($3)), ($4), ($5)
        );
        """, user_id, user_name, user_role, user_phone, user_document
    )
    await db_conn.execute(*sql)


async def save_to_blacklist(db_conn: asyncpg.Connection,
                            *,
                            user_id: int,
                            user_name: str,
                            user_phone: str,
                            **kwargs):
    sql = (
        f"""
        INSERT INTO blacklist (tg_id, name, phone) VALUES (
            ($1), ($2), ($3)
        );
        """, user_id, user_name, user_phone
    )
    await db_conn.execute(*sql)
