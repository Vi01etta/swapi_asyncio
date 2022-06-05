from contextlib import asynccontextmanager

from sqlalchemy.dialects.postgresql import insert

import app
from sqlalchemy import Column, String, Integer
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Characters(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    birth_year = Column(String())
    eye_color = Column(String())
    films = Column(String())
    gender = Column(String())
    hair_color = Column(String())
    height = Column(String())
    homeworld = Column(String())
    mass = Column(String())
    name = Column(String())
    species = Column(String())
    skin_color = Column(String())
    starships = Column(String())
    vehicles = Column(String())


engine = create_async_engine('postgresql+asyncpg://admin:1234@localhost/starwars', echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            for hero in app.heroes:
                if 'name' in hero:
                    query_data = {'id': int(hero['url'].split('/')[-2]),
                                  'birth_year': hero['birth_year'],
                                  'eye_color': hero['eye_color'],
                                  'films': ', '.join(hero['films']),
                                  'gender': hero['gender'],
                                  'hair_color': hero['hair_color'],
                                  'height': hero['height'],
                                  'homeworld': hero['homeworld'],
                                  'mass': hero['mass'],
                                  'name': hero['name'],
                                  'species': ', '.join(hero['species']),
                                  'skin_color': hero['skin_color'],
                                  'starships': ', '.join(hero['starships']),
                                  'vehicles': ', '.join(hero['vehicles'])
                                  }
                    query = insert(Characters).values(query_data)
                    await session.execute(query)
        await session.commit()


asyncio.run(async_main())
