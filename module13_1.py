import asyncio

BALL_COUNT = 5
BASE_DELAY = 2

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования')
    for ball_n in range(BALL_COUNT):
        await asyncio.sleep(BASE_DELAY / power)
        print(f'Силач {name} поднял {ball_n + 1}')
    print(f'Силач {name} закончил соревнования')

async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task1
    await task2
    await task3

asyncio.run(start_tournament())
