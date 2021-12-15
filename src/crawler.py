import json
import time

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
            try:
                soup = BeautifulSoup(response.json()["content"], "html.parser")
            except:
                continue
            urls = soup.findAll("a", {"class": "cover anime-tooltip"})
            for new in urls:
                url = new["href"]
                print(url)
                response_url = requests.get(
                    url,
                    headers=headers,
                    timeout=10
                )
                if not response_url.ok:
                    time.sleep(2)
                    response_url = requests.get(
                        url,
                        headers=headers,
                        timeout=10
                    )
                    if not response_url.ok:
                        continue
                soup = BeautifulSoup(response_url.text, "html.parser")
                div_name = soup.find("header", {"class": "head"})
                name = div_name('meta')[0]["content"]
                print(name)
                div_image = soup.find("div", {"class": "c-poster"})
                image_url = div_image('img')[0]["src"]
                div = soup.findAll("div", {"class": "value"})
                try:
                    type = div[0].text.strip()
                except:
                    type = None
                try:
                    current_episodes = div[1].text.strip().split(" /")[0]
                except:
                    current_episodes = None
                try:
                    total_episodes = div[1].text.strip().split(" /")[1]
                except:
                    total_episodes = None
                try:
                    next_episode_date = div[2].text.strip()
                except:
                    next_episode_date = None
                try:
                    started = div[4].text.strip()
                except:
                    started = None
                try:
                    for _i in div[5]:
                        genres = _i.find("span", {"class": "genre-ru"}).text
                except:
                    try:
                        for _i in div[4]:
                            genres = _i.find("span", {"class": "genre-ru"}).text
                    except:
                        try:
                            for _i in div[3]:
                                genres = _i.find("span", {"class": "genre-ru"}).text
                        except:
                            genres = None
                try:
                    rating = div[6].text.strip()
                except:
                    rating = None
                try:
                    licensed_by = div[7].text.strip()
                except:
                    licensed_by = None
                div_name_rus = soup.find("header", {"class": "head"})
                try:
                    name_rus = div_name_rus.find('h1').text.strip().split(" /")[0]
                except:
                    name_rus = None
                div_rating = soup.find("div", {"class": "score-value score-9"})
                try:
                    score = div_rating.text.strip()
                except:
                    score = None
                div_description = soup.find("div", {"class": "b-text_with_paragraphs"})
                try:
                    description = div_description.text.strip()
                except:
                    description = None
                div_studio = soup.findAll("div", {"class": "block"})
                try:
                    studio = div_studio[5]("img")[0]["alt"]
                except:
                    studio = None
                related_url = url + "/resources"
                response_related_url = requests.get(
                    related_url,
                    headers=headers,
                    timeout=10
                )
                soup_related = BeautifulSoup(response_related_url.text, "html.parser")
                # div_related = soup_related.find("div", class_="b-db_entry-variant-list_item")["data-url"]
                div_related = soup_related.find("div", class_="c-column block_m").findAll(class_="b-db_entry-variant-list_item")
                related = []
                for i in div_related:
                    related.append(i["data-url"]) #creating list, use it in searching urls; and what retries create it in a function; also try/except to if else

                print(related)

                div_author = soup_related.find("div", {"class": "c-column c-authors block_m"})
                print(div_author)


                div_other_names = soup.find("span", {"class": "other-names"})
                url_name_alt = div_other_names["data-clickloaded-url"]
                response_url_name_alt = requests.get(
                    url_name_alt,
                    headers=headers,
                    timeout=10
                )
                soup = BeautifulSoup(response_url_name_alt.text, "html.parser")
                div_name_alt = soup.findAll("div", {"class": "value"})
                try:
                    name_alt = div_name_alt[2].text.strip()
                except:
                    name_alt = None
                id = url.split("/")[-1].split("-")[0]
                data.append(
                    Anime(
                        url=url,
                        id=id,  #url.split("/")[-1].split("-")[0]
                        name=name,
                        image_url=image_url,
                        name_rus=name_rus,
                        name_alt=name_alt,
                        type=type,
                        total_episodes=total_episodes,
                        current_episodes=current_episodes,
                        next_episode_date=next_episode_date,
                        started=started,
                        genres=genres,
                        score=score,
                        rating=rating,
                        licensed_by=licensed_by,
                        studio=studio,
                        description=description,

                    )
                )


def parse_character():
    pass


def parse_staff():
    pass


def parse_studio():
    pass


if __name__ == "__main__":
    start = parse_anime()
    print(start)

