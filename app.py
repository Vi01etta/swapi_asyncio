import aiohttp

import asyncio
from more_itertools import chunked

URL = 'https://swapi.dev/api/people/'

MAX = 80
PARTITION = 10


async def get_person(person_id, session):
    async with session.get(f'{URL}{person_id}') as response:
        return await response.json()


async def get_people(all_ids, partition, session):
    for chunk_ids in chunked(all_ids, partition):
        tasks = [asyncio.create_task(get_person(person_id, session)) for person_id in chunk_ids]
        for task in tasks:
            task_result = await task
            yield task_result


async def main():
    async with aiohttp.ClientSession() as session:
        people_data = []
        async for people in get_people(range(1, MAX + 1), PARTITION, session):
            people_data.append(people)
        return people_data



heroes = asyncio.run(main())