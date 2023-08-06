from .db import CREATE_TABLE_QUERY


class Base:
    def __init__(self, pool):
        self.pool = pool
        self.table_exists = False

    async def ensure_table_exists(self, conn):
        if not self.table_exists:
            await conn.execute(CREATE_TABLE_QUERY)
            self.table_exists = True
