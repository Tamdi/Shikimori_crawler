ANIME_URL = "https://shikimori.one/animes/status/ongoing/page/"
API_HOST = "0.0.0.0"
API_PORT = "8083"
INSECURE_PORT = "[::]:8080"
PORT = 8088
POSTGRES_URL = 'postgresql://postgres:1@localhost:5432/postgres'
ANIME_TABLE = "anime"
CHARACTER_TABLE = "character"
STUDIO_TABLE = "studio"
STAFF_TABLE = "staff"
headers = {
    'authority': 'shikimori.one',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0 SEB',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}
