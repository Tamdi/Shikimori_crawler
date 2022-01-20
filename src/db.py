import json
import sqlalchemy.exc
from sqlalchemy import create_engine, MetaData, Table, Column, String, ARRAY
from config import POSTGRES_URL, ANIME_TABLE, STAFF_TABLE, STUDIO_TABLE, CHARACTER_TABLE


def saver_character(character_list):
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    character_model = Table(
        CHARACTER_TABLE, meta,
        Column('id', String, primary_key=True),
        Column('url', String),
        Column('name', String),
        Column('name_rus', String),
        Column('image_url', String)
    )
    meta.create_all(engine)
    anime_list = json.loads(character_list)
    for new in anime_list:
        result = character_model.insert().values(
            id=new.id,
            url=new.url,
            name=new.name,
            name_rus=new.name_rus,
            image_url=new.image_url
        )
        conn = engine.connect()
    try:
        res = conn.execute(result)
    except sqlalchemy.exc.IntegrityError:
        print("this data already exists")


def saver_staff(staff_list):
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    anime_model = Table(
        STAFF_TABLE, meta,
        Column('id', String, primary_key=True),
        Column('url', String),
        Column('name', String),
        Column('name_rus', String),
        Column('occupation', String),
        Column('image_url', String)
    )
    meta.create_all(engine)
    anime_list = json.loads(staff_list)
    for new in anime_list:
        result = anime_model.insert().values(
            id=new.id,
            url=new.url,
            name=new.name,
            name_rus=new.name_rus,
            occupation=new.occupation,
            image_url=new.image_url
        )
        conn = engine.connect()
    try:
        res = conn.execute(result)
    except sqlalchemy.exc.IntegrityError:
        print("this data already exists")


def saver_studio(studio_list):
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    anime_model = Table(
        STUDIO_TABLE, meta,
        Column('id', String, primary_key=True),
        Column('url', String),
        Column('name', String),
        Column('image_url', String)
    )
    meta.create_all(engine)
    anime_list = json.loads(studio_list)
    for new in anime_list:
        result = anime_model.insert().values(
            id=new.id,
            url=new.url,
            name=new.name,
            image_url=new.image_url
        )
        conn = engine.connect()
    try:
        res = conn.execute(result)
    except sqlalchemy.exc.IntegrityError:
        print("this data already exists")


def saver_anime(anime_list):
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    anime_model = Table(
        ANIME_TABLE, meta,
        Column('id', String, primary_key=True),
        Column('url', String),
        Column('name', String),
        Column('name_rus', String),
        Column('name_alt', String),
        Column('type', String),
        Column('total_episodes', int),
        Column('current_episodes', String),
        Column('next_episode_date', String),
        Column('started', String),
        Column('genres', String),
        Column('score', String),
        Column('rating', String),
        Column('licensed_by', String),
        Column('studio', ARRAY, foreign_key=True),
        Column('description', String),
        Column('related', ARRAY),
        Column('author', ARRAY, foreign_key=True),
        Column('main_heroes', ARRAY, foreign_key=True),
        Column('scenes', ARRAY),
        Column('videos', ARRAY),
        Column('similar', ARRAY),
        Column('image_url', String)
    )
    meta.create_all(engine)
    anime_list = json.loads(anime_list)
    for new in anime_list:
        result = anime_model.insert().values(
            id=new.id,
            url=new.url,
            name=new.name,
            name_rus=new.name_rus,
            name_alt=new.name_alt,
            type=new.type,
            total_episodes=new.total_episodes,
            current_episodes=new.current_episodes,
            next_episode_date=new.next_episode_date,
            started=new.started,
            genres=new.genres,
            score=new.score,
            rating=new.rating,
            licensed_by=new.licensed_by,
            studio=new.studio,
            description=new.description,
            related=new.related,
            author=new.author,
            main_heroes=new.main_heroes,
            scenes=new.scenes,
            videos=new.videos,
            similar=new.similar,
            image_url=new.image_url
        )
        conn = engine.connect()
    try:
        res = conn.execute(result)
    except sqlalchemy.exc.IntegrityError:
        print("this data already exists")


def get_data_anime():
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    meta.create_all(engine)
    result = engine.execute(f"SELECT * FROM {ANIME_TABLE}")
    res = []
    for i in result:
        data = {
            'id': i[0],
            'url': i[1],
            'name': i[2],
            'name_rus': i[3],
            'name_alt': i[4],
            'type': i[5],
            'total_episodes': i[6],
            'current_episodes': i[7],
            'next_episode_date': i[8],
            'started': i[9],
            'genres': i[10],
            'score': i[11],
            'rating': i[12],
            'licensed_by': i[13],
            'studio': i[14],
            'description': i[15],
            'related': i[16],
            'author': i[17],
            'main_heroes': i[18],
            'scenes': i[19],
            'videos': i[20],
            'similar': i[21],
            'image_url': i[22]
        }
        res.append(data)
    return res


def get_data_studio():
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    meta.create_all(engine)
    result = engine.execute(f"SELECT * FROM {STUDIO_TABLE}")
    res = []
    for i in result:
        data = {
            'id': i[0],
            'url': i[1],
            'name': i[2],
            'image_url': i[3]
        }
        res.append(data)
    return res


def get_data_staff():
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    meta.create_all(engine)
    result = engine.execute(f"SELECT * FROM {STAFF_TABLE}")
    res = []
    for i in result:
        data = {
            'id': i[0],
            'url': i[1],
            'name': i[2],
            'name_rus': i[3],
            'occupation': i[4],
            'image_url': i[5]
        }
        res.append(data)
    return res


def get_data_character():
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    meta.create_all(engine)
    result = engine.execute(f"SELECT * FROM {CHARACTER_TABLE}")
    res = []
    for i in result:
        data = {
            'id': i[0],
            'url': i[1],
            'name': i[2],
            'name_rus': i[3],
            'image_url': i[4]
        }
        res.append(data)
    return res

