import json
import requests
from models import Anime, Character, Staff, Studio
from config import ANIME_URL
from bs4 import BeautifulSoup


def parse_anime():
    headers = {
        'authority': 'shikimori.one',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0 SEB',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    response = requests.get(
        ANIME_URL+"1.json",
        headers=headers,
        timeout=10
    )
    LatinAlphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"
    RusUpperAlphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    related = ""
    if response.ok:
        data = []
        json_data = response.json()
        pages_count = json_data["pages_count"]
        for _i in range(pages_count):
            response = requests.get(
                ANIME_URL + str(_i) + ".json",
                headers=headers,
                timeout=10
            )
            soup = BeautifulSoup(response.json()["content"], "html.parser")
            urls = soup.findAll("a", {
                "class": "cover anime-tooltip"
            })
            for new in urls:
                url = new["href"]
                response_url = requests.get(
                    url,
                    headers=headers,
                    timeout=10
                )
                soup = BeautifulSoup(response_url.text, "html.parser")
                div = soup.find("div", {
                    "class": "c-poster"
                })
                name = div('img')[0]["title"]
                image_url = div('img')[0]["src"]
                div = soup.findAll("div", {
                    "class": "value"
                })
                type = div[0].text.strip()
                current_episodes = div[1].text.strip().split(" /")[0]
                try:
                    total_episodes = div[1].text.strip().split(" /")[1]
                except:
                    total_episodes = None

                # print(total_episodes)
                next_episode_date = div[2].text.strip()
                started = div[4].text.strip()
                genres = div[5].text.strip()
                # for _i in genres:
                #     # print(_i.find("span", {"class": "genre-ru"}))
                #     print("span", _i)
                for specialChar in LatinAlphabet:
                    genres = genres.replace(specialChar, '')
                for specialChar in RusUpperAlphabet:
                    genres = genres.replace(specialChar, ' '+specialChar)
                try:
                    rating = div[6].text.strip()
                except:
                    rating = None
                try:
                    licensed_by = div[7].text.strip()
                except:
                    licensed_by = None
                div_name_rus = soup.find("header", {"class": "head"})
                name_rus = div_name_rus.find('h1').text.strip().split(" /")[0]
                div_rating = soup.find("div", {"class": "score-value score-9"})
                try:
                    score = div_rating.text.strip()
                except:
                    score = None
                try:
                    div_description = soup.find("div", {"class": "b-text_with_paragraphs"})
                    description = div_description.text.strip()
                except:
                    description = None
                div_studio = soup.findAll("div", {"class": "block"})
                studio = div_studio[5]("img")[0]["alt"]

                # div_related = soup.find("div", {
                #     "class": "c-column block_m"
                # })
                # print(div_related)
                div_author = soup.find("div", {"class": "b-db_entry-variant-list_item"})
                print(div_author)


                div_other_names = soup.find("span", {
                    "class": "other-names"
                })
                url_name_alt = div_other_names["data-clickloaded-url"]
                response_url_name_alt = requests.get(
                    url_name_alt,
                    headers=headers,
                    timeout=10
                )
                soup = BeautifulSoup(response_url_name_alt.text, "html.parser")
                div_name_alt = soup.findAll("div", {
                    "class": "value"
                })
                name_alt = div_name_alt[2].text.strip()
                id=url.split("/")[-1].split("-")[0]
                print(id, url)
                data.append(
                    Anime(
                        url=url,
                        id=url.split("/")[-1].split("-")[0],
                        name=name,
                        image_url=image_url,
                    )
                )
                print(data[0])






def parse_character():
    pass


def parse_staff():
    pass


def parse_studio():
    pass


if __name__ == "__main__":
    start = parse_anime()
    print(start)

