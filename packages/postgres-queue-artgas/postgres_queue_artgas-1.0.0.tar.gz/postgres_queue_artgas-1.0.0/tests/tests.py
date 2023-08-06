from postgres_queue_artgas import Master, Worker
import asyncpg
import asyncio


async def task_handler(string1, string2):
    print(string1, string2)


async def main():
    pool = await asyncpg.create_pool(database='postgres',
                                     user='postgres',
                                     password='k3k1n6_0nl1n3',
                                     )
    master = Master(pool)
    await master.publish('test', string1='a', string2='b')
    worker = Worker(pool=pool)
    await worker.consume('test', task_handler)
    await asyncio.Future()


asyncio.run(main())
