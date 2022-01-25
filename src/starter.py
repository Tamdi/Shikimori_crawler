import grpc
from src.proto.shikimori_pb2_grpc import AnimeCrawlerServicer, add_AnimeCrawlerServicer_to_server
from src.proto.shikimori_pb2 import AnimeResponse, Anime, StaffResponse, Staff, StudioResponse, Studio, CharactersResponse, Characters
from crawler import parse_anime, parse_staff, parse_studio, parse_characters
from concurrent import futures


class Service(AnimeCrawlerServicer):
    def GetAnime(self, request, context):
        data_anime = parse_anime()
        anime = []
        for n in data_anime:
            anime.append(
                Anime(
                    id=n.id,
                    url=n.url,
                    name=n.name,
                    name_rus=n.name_rus,
                    name_alt=n.name_alt,
                    type=n.type,
                    total_episodes=n.total_episodes,
                    current_episodes=n.current_episodes,
                    next_episode_date=n.next_episode_date,
                    started=n.started,
                    genres=n.genres,
                    score=n.score,
                    rating=n.rating,
                    licensed_by=n.licensed_by,
                    # studio=n.studio,
                    description=n.description,
                    # related=n.related,
                    # author=n.author,
                    # main_heroes=n.main_heroes,
                    # scenes=n.scenes,
                    # videos=n.videos,
                    # similar=n.similar,
                    image_url=n.image_url
                )
            )
        return AnimeResponse(
            anime=anime
        )

    def GetStaff(self, request, context):
        data_staff = parse_staff()
        staff = []
        for n in data_staff:
            staff.append(
                Staff(
                    url=n.url,
                    id=n.id,
                    name=n.name,
                    name_rus=n.name_rus,
                    occupation=n.occupation,
                    image_url=n.image_url,
                )
            )
        return StaffResponse(
            staff=staff
        )

    def GetStudio(self, request, context):
        data_studio = parse_studio()
        studio = []
        for n in data_studio:
            studio.append(
                Studio(
                    url=n.url,
                    id=n.id,
                    name=n.name,
                    image_url=n.image_url,
                )
            )
        return StudioResponse(
            studio=studio
        )

    def GetCharacters(self, request, context):
        data_characters = parse_characters()
        characters = []
        for n in data_characters:
            characters.append(
                Characters(
                    url=n.url,
                    id=n.id,
                    name=n.name,
                    name_rus=n.name_rus,
                    image_url=n.image_url,
                )
            )
        return CharactersResponse(
            characters=characters
        )


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_AnimeCrawlerServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:8080')
    print("Starting grpc server...")
    server.start()
    server.wait_for_termination()
