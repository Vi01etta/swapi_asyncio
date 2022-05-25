from sqlalchemy import Column, String, Integer, create_engine
import asyncio
import aiohttp

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import app

conn = 'postgresql://admin:1234@localhost/starwars'
engine = create_engine(conn)
r = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)


class CharModel(Base):
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


Base.metadata.create_all(engine)


async def post():
    new_ad_data = await app.main()
    # как подключиться к базе данных
    query_data = {'id' : int(new_ad_data['url'].split('/')[-2]),
        'birth_year' : new_ad_data['birth_year'],
        'eye_color' : new_ad_data['eye_color'],
        'films' : ', '.join(new_ad_data['films']),
        'gender' : new_ad_data['gender'],
        'hair_color' : new_ad_data['hair_color'],
        'height' : new_ad_data['height'],
        'homeworld' : new_ad_data['homeworld'],
        'mass' : new_ad_data['mass'],
        'name' : new_ad_data['name'],
        'species' : ', '.join(new_ad_data['species']),
        'skin_color' : new_ad_data['skin_color'],
        'starships' : ', '.join(new_ad_data['starships']),
        'vehicles' : ', '.join(new_ad_data['vehicles'])
    }
    await CharModel.insert(query_data).execute()


asyncio.run(post())
