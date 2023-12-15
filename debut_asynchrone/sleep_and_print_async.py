import asyncio

async def count_to_10():
    for i in range(1, 11):
        print(i)
        await asyncio.sleep(0.5)


loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(count_to_10()),
    loop.create_task(count_to_10())
]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()