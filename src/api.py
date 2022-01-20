import grpc
import json
from src.proto.shikimori_pb2_grpc import AnimeCrawlerStub
from src.proto.shikimori_pb2 import AnimeRequest, StudioRequest, StaffRequest, CharactersRequest
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
                    'studio': n.studio,
                    'description': n.description,
                    'related': n.related,
                    'author': n.author,
                    'main_heroes': n.main_heroes,
                    'scenes': n.scenes,
                    'videos': n.videos,
                    'similar': n.similar,
                    'image_url': n.image_url,
                }
            )

        result = json.dumps(anime, ensure_ascii=False)
        saver_anime(result)
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
        result = json.dumps(staff, ensure_ascii=False)
        saver_staff(result)
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


@get('/staff')
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
        result = json.dumps(characters, ensure_ascii=False)
        saver_character(result)
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
    print("Started")
    run(host='0.0.0.0', port=8082)
