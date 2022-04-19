import grpc
import json
import logging
from src.proto.shikimori_pb2_grpc import AnimeCrawlerStub
from src.proto.shikimori_pb2 import AnimeRequest, StudioRequest, StaffRequest, CharactersRequest
from config import API_PORT, API_HOST
from bottle import get, run
from db import saver_character, saver_staff, saver_studio, saver_anime, get_data_anime, get_data_character, get_data_studio, get_data_staff


@get('/anime')
def return_anime():
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = AnimeCrawlerStub(channel)
        response_anime = stub.GetAnime(
            AnimeRequest())
        anime = []
        for n in response_anime.anime:
            studio_list_of_dict = [{
                "url": _studio.url,
                'id': _studio.id,
                'name': _studio.name,
                'image_url': _studio.image_url,
            }for _studio in n.studio]
            character_list_of_dict = [{
                "url": _main_heroes.url,
                'id': _main_heroes.id,
                'name': _main_heroes.name,
                'name_rus': _main_heroes.name_rus,
                'image_url': _main_heroes.image_url,
            } for _main_heroes in n.main_heroes]
            staff_list_of_dict = [{
                "url": _author.url,
                'id': _author.id,
                'name': _author.name,
                'name_rus': _author.name_rus,
                'occupation': _author.occupation,
                'image_url': _author.image_url,
            } for _author in n.author]
            anime.append(
                {
                    'url': n.url,
                    'id': n.id,
                    'name': n.name,
                    'name_rus': n.name_rus,
                    'name_alt': n.name_alt,
                    'type': n.type,
                    'total_episodes': n.total_episodes,
                    'current_episodes': n.current_episodes,
                    'next_episode_date': n.next_episode_date,
                    'started': n.started,
                    'genres': n.genres,
                    'score': n.score,
                    'rating': n.rating,
                    'licensed_by': n.licensed_by,
                    'studio': studio_list_of_dict,
                    'description': n.description,
                    'related': n.related,
                    'author': staff_list_of_dict,
                    'main_heroes': character_list_of_dict,
                    'scenes': n.scenes,
                    'videos': n.videos,
                    'similar': n.similar,
                    'image_url': n.image_url,
                }
            )

        result = json.dumps(json.loads(f'{anime}'.replace("\'", '\"')), ensure_ascii=False)
        # saver_anime(result)
        return result


@get('/staff')
def return_staff():
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = AnimeCrawlerStub(channel)
        response_staff = stub.GetStaff(
            StaffRequest())
        staff = []
        for n in response_staff.staff:
            staff.append(
                {
                    "url": n.url,
                    'id': n.id,
                    'name': n.name,
                    'name_rus': n.name_rus,
                    'occupation': n.occupation,
                    'image_url': n.image_url,
                }
            )
        result = json.dumps(json.loads(f'{staff}'.replace("\'", '\"')), ensure_ascii=False)
        # saver_staff(result)
        return result


@get('/studio')
def return_studio():
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = AnimeCrawlerStub(channel)
        response_studio = stub.GetStudio(
            StudioRequest())
        studio = []
        for n in response_studio.studio:
            studio.append(
                {
                    "url": n.url,
                    'id': n.id,
                    'name': n.name,
                    'image_url': n.image_url,
                }
            )
        result = json.dumps(studio, ensure_ascii=False)
        saver_studio(result)
        return result


@get('/character')
def return_character():
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = AnimeCrawlerStub(channel)
        response_character = stub.GetCharacters(
            CharactersRequest())
        characters = []
        for n in response_character.characters:
            characters.append(
                {
                    "url": n.url,
                    'id': n.id,
                    'name': n.name,
                    'name_rus': n.name_rus,
                    'image_url': n.image_url,

                }
            )
        result = json.dumps(json.loads(f'{characters}'.replace("\'", '\"')), ensure_ascii=False)
        # saver_character(result)
        return result


@get('/saved_anime')
def get_saved_anime():
    return json.dumps(get_data_anime(), ensure_ascii=False)


@get('/saved_characters')
def get_saved_characters():
    return json.dumps(get_data_character(), ensure_ascii=False)


@get('/saved_staff')
def get_saved_staff():
    return json.dumps(get_data_staff(), ensure_ascii=False)


@get('/saved_studio')
def get_saved_studio():
    return json.dumps(get_data_studio(), ensure_ascii=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting api...")
    run(host=API_HOST, port=API_PORT)
