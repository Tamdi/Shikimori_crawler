import grpc
from src.proto.shikimori_pb2_grpc import AnimeCrawlerStub
from src.proto.shikimori_pb2 import AnimeRequest, StudioRequest, StaffRequest, CharactersRequest
from config import INSECURE_PORT


if __name__ == '__main__':
    with grpc.insecure_channel(INSECURE_PORT) as channel:
        stub = AnimeCrawlerStub(channel)
        response_anime: AnimeRequest = stub.GetAnime(AnimeRequest(id=1))
        for n in response_anime.anime:
            print(f'Id: {n.id}')
            print(f'Url: {n.url}')
            print(f'Name: {n.name}')
            print(f'Name_rus: {n.name_rus}')
            print(f'Name_alt: {n.name_alt}')
            print(f'Name_alt: {n.type}')
            print(f'Total_episodes: {n.total_episodes}')
            print(f'Current_episodes: {n.current_episodes}')
            print(f'Next_episode_date: {n.next_episode_date}')
            print(f'Started: {n.started}')
            print(f'Genres: {n.genres}')
            print(f'Score: {n.score}')
            print(f'Rating: {n.rating}')
            print(f'Licensed_by: {n.licensed_by}')
            print(f'Studio: {n.studio}')
            print(f'Description: {n.description}')
            print(f'Related: {n.related}')
            print(f'Author: {n.author}')
            print(f'Main_heroes: {n.main_heroes}')
            print(f'Scenes: {n.scenes}')
            print(f'Videos: {n.videos}')
            print(f'Similar: {n.similar}')
            print(f'Image_url: {n.image_url}')

        response_staff = stub.GetStaff(StaffRequest(id=1))
        for n in response_staff.staff:
            print("----")
            print(f'Url: {n.url}')
            print(f'Id: {n.id}')
            print(f'Name: {n.name}')
            print(f'Name_rus: {n.name_rus}')
            print(f'Occupation: {n.occupation}')
            print(f'Image_url: {n.image_url}')

        response_studio = stub.GetStudio(StudioRequest(id=1))
        for n in response_studio.studio:
            print("----")
            print(f'Url: {n.url}')
            print(f'Id: {n.id}')
            print(f'Name: {n.name}')
            print(f'Image_url: {n.image_url}')

        response_characters = stub.GetCharacters(CharactersRequest(id=1))
        for n in response_characters.characters:
            print("----")
            print(f'Url: {n.url}')
            print(f'Id: {n.id}')
            print(f'Name: {n.name}')
            print(f'Name_rus: {n.name_rus}')
            print(f'Image_url: {n.image_url}')