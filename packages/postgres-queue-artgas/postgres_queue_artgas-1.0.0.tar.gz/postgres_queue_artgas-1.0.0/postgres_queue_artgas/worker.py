import asyncio
import json
from .base import Base
from typing import Callable, Awaitable
from .db import QUERY_TAKE_TASK, UPDATE_FINISHED_TASK_QUERY


class Worker(Base):
    def __init__(self, *, poll_interval: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.poll_interval = poll_interval

    async def consume(self, queue_name: str, handler: Callable[[...], Awaitable[None]]):
        while True:
            async with self.pool.acquire() as conn:
                await self.ensure_table_exists(conn)
                task = await conn.fetchrow(QUERY_TAKE_TASK, queue_name)
            if not task:
                await asyncio.sleep(self.poll_interval)
                continue
            task_id = task['id']
            task_data = json.loads(task["data"])
            try:
                await handler(**task_data)
            finally:
                async with self.pool.acquire() as conn:
                    await conn.fetch(UPDATE_FINISHED_TASK_QUERY, task_id)
