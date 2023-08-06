import json
from .db import PUT_TASK_QUERY
from .base import Base


class Master(Base):
    async def publish(self, queue_name, **kwargs):
        async with self.pool.acquire() as conn:
            await self.ensure_table_exists(conn)
            await conn.execute(PUT_TASK_QUERY, queue_name, json.dumps(kwargs))
