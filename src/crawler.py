import time
import requests
from models import Anime, Character, Staff, Studio
from config import ANIME_URL
from bs4 import BeautifulSoup

headers = {
    'authority': 'shikimori.one',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0 SEB',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}


def anime_urls():
    url_list = []
    response = requests.get(
        ANIME_URL + "1.json",
        headers=headers,
        timeout=10
    )
    if response.ok:
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
                url_list.append(url)
    return url_list


def p_characters(url):
    data = []
    while True:
        id = []
        name = []
        name_rus = []
        image_url = []
        print("character", url)
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
        resources_url = url + "/resources"
        response_resources_url = requests.get(
            resources_url,
            headers=headers,
            timeout=10
        )
        soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")
        try:
            div_character = soup_resources.find("div", {"class": "cc-characters"}).find("div", {"class": "cc m0 to-process"})
        except:
            continue
        try:
            div_image_url = div_character.find("span", {"class": "image-cutter"})
        except:
            continue
        try:
            div_name = div_character.find("span", {"class": "name-en"})
        except:
            continue
        try:
            div_name_rus = div_character.find("span", {"class": "name-ru"})
        except:
            continue
        for i in div_character:
            try:
                id.append(i["id"])
            except:
                id.append(None)
        for i in div_name:
            try:
                name.append(i)
            except:
                name.append(None)
        for i in div_name_rus:
            try:
                name_rus.append(i)
            except:
                name_rus.append(None)
        for i in div_image_url:
            try:
                image_url.append(i["src"])
            except:
                image_url = None
        data.append(
            Character(
                url=url,
                id=id,
                name=name,
                name_rus=name_rus,
                image_url=image_url
            )
        )
        break
    return data


def p_staff(url):
    data = []
    while True:
        id = []
        name = []
        name_rus = []
        occupations = []
        image_url = []
        print("staff", url)
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
        resources_url = url + "/resources"
        response_resources_url = requests.get(
            resources_url,
            headers=headers,
            timeout=10
        )
        soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")
        div_authors = soup_resources.find("div", {"class": "c-column c-authors block_m"})
        try:
            div_id = div_authors.findAll("div", {"class": "b-db_entry-variant-list_item"})
        except:
            continue
        try:
            div_name = div_authors.findAll("span", {"class": "name-en"})
        except:
            continue
        try:
            div_name_rus = div_authors.findAll("span", {"class": "name-ru"})
        except:
            continue
        try:
            div_image_url = div_authors.findAll("div", {"class": "image linkeable bubbled"})
        except:
            continue
        for i in div_id:
            try:
                id.append(i["data-id"])
            except:
                id.append(None)
        for i in div_name:
            try:
                name.append(i.text)
            except:
                name.append(None)
        for i in div_name_rus:
            try:
                name_rus.append(i.text)
            except:
                name_rus.append(None)
        for author_div in soup_resources.find_all("div", {"class": "b-db_entry-variant-list_item", "data-type": "person"}):
            a = [btag.text for btag in author_div.find_all("div", {"class": "b-tag"}) if len(btag["class"]) == 1]
            try:
                occupations.append(", ".join(a))
                # list comprehension, data-type, bd доделать исатфф с каэрэктер
            except:
                occupations.append(None)
        for i in div_image_url:
            try:
                image_url.append(i("img")[0]["src"])
            except:
                image_url.append(None)
        data.append(
            Staff(
                url=url,
                id=id,
                name=name,
                name_rus=name_rus,
                occupation=occupations,
                image_url=image_url
            )
        )
        break
    return data


def p_studio(url):
    data = []
    while True:
        print("studio", url)
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
        div_studio = soup.findAll("div", {"class": "block"})
        try:
            url = div_studio[5]("a")[0]["href"]
        except:
            url = None
        try:
            id = url.split("/")[-1].split("-")[0]
        except:
            id = None
        try:
            name = div_studio[5]("img")[0]["alt"]
        except:
            name =None
        try:
            image_url = div_studio[5]("img")[0]["src"]
        except:
            image_url = None
        data.append(
            Studio(
                url=url,
                id=id,
                name=name,
                image_url=image_url
            )
        )
        break
    return data


def parse_anime():
    data = []
    urls = anime_urls()
    for url in urls:
        related = []
        scenes = []
        videos = []
        similar = []
        print("anime", url)
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
            total_episodes = int(div[1].text.strip().split(" /")[1])
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
        if div_name_rus.find('h1') is not None:
            name_rus = div_name_rus.find('h1').text.strip().split(" /")[0]
        else:
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

        resources_url = url + "/resources"
        response_resources_url = requests.get(
            resources_url,
            headers=headers,
            timeout=10
        )
        soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")
        try:
            div_related = soup_resources.find("div", class_="c-column block_m").findAll(class_="b-db_entry-variant-list_item")
        except:
            continue
        try:
            div_scenes = soup_resources.find("div", class_="c-screenshots").find(class_="cc")
        except:
            continue
        try:
            div_videos = soup_resources.find("div", class_="c-videos").find(class_="cc").findAll(class_="video-link")
        except:
            continue
        try:
            div_similar = soup_resources.find("div", class_="cc cc-similar to-process").findAll(class_="title two_lined")
        except:
            continue
        for i in div_related:
            try:
                related.append(i["data-url"])
            except:
                related.append(None)
        for i in div_scenes:
            try:
                scenes.append(i["href"])
            except:
                scenes.append(None)
        for i in div_videos:
            try:
                videos.append(i["href"])
            except:
                videos.append(None)
        for i in div_similar:
            try:
                similar.append(i["href"])
            except:
                similar.append(None)
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
        studio: list[Studio]
        author: list[Staff]
        main_heroes: list[Character]
        author = p_staff(url)
        print(author)
        studio = p_studio(url)
        print(studio)
        main_heroes = p_characters(url)
        print(main_heroes)
        id = url.split("/")[-1].split("-")[0]
        data.append(
            Anime(
                url=url,
                id=id,  # url.split("/")[-1].split("-")[0]
                name=name,
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
                related=related,
                author=author,
                main_heroes=main_heroes,
                scenes=scenes,
                videos=videos,
                similar=similar,
                image_url=image_url,
            )
        )
    return data


def parse_characters():
    data = []
    urls = anime_urls()
    for url in urls:
        id = []
        name = []
        name_rus = []
        image_url = []
        print("character", url)
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
        resources_url = url + "/resources"
        response_resources_url = requests.get(
            resources_url,
            headers=headers,
            timeout=10
        )
        soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")
        try:
            div_character = soup_resources.find("div", {"class": "cc-characters"}).find("div", {"class": "cc m0 to-process"})
        except:
            continue
        try:
            div_image_url = div_character.find("span", {"class": "image-cutter"})
        except:
            continue
        try:
            div_name = div_character.find("span", {"class": "name-en"})
        except:
            continue
        try:
            div_name_rus = div_character.find("span", {"class": "name-ru"})
        except:
            continue
        for i in div_character:
            try:
                id.append(i["id"])
            except:
                id.append(None)
        for i in div_name:
            try:
                name.append(i)
            except:
                name.append(None)
        for i in div_name_rus:
            try:
                name_rus.append(i)
            except:
                name_rus.append(None)
        for i in div_image_url:
            try:
                image_url.append(i["src"])
            except:
                image_url = None
        data.append(
            Character(
                url=url,
                id=id,
                name=name,
                name_rus=name_rus,
                image_url=image_url
            )
        )
    return data


def parse_staff():
    data = []
    urls = anime_urls()
    for url in urls:
        id = []
        name = []
        name_rus = []
        occupations = []
        image_url = []
        print("staff", url)
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
        resources_url = url + "/resources"
        response_resources_url = requests.get(
            resources_url,
            headers=headers,
            timeout=10
        )
        soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")
        div_authors = soup_resources.find("div", {"class": "c-column c-authors block_m"})
        try:
            div_id = div_authors.findAll("div", {"class": "b-db_entry-variant-list_item"})
        except:
            continue
        try:
            div_name = div_authors.findAll("span", {"class": "name-en"})
        except:
            continue
        try:
            div_name_rus = div_authors.findAll("span", {"class": "name-ru"})
        except:
            continue
        try:
            div_image_url = div_authors.findAll("div", {"class": "image linkeable bubbled"})
        except:
            continue
        for i in div_id:
            try:
                id.append(i["data-id"])
            except:
                id.append(None)
        for i in div_name:
            try:
                name.append(i.text)
            except:
                name.append(None)
        for i in div_name_rus:
            try:
                name_rus.append(i.text)
            except:
                name_rus.append(None)
        for author_div in soup_resources.find_all("div", {"class": "b-db_entry-variant-list_item", "data-type": "person"}):
            a = [btag.text for btag in author_div.find_all("div", {"class": "b-tag"}) if len(btag["class"]) == 1]
            try:
                occupations.append(", ".join(a))
                # list comprehension, data-type, bd доделать исатфф с каэрэктер
            except:
                occupations.append(None)
        for i in div_image_url:
            try:
                image_url.append(i("img")[0]["src"])
            except:
                image_url.append(None)
        data.append(
            Staff(
                url=url,
                id=id,
                name=name,
                name_rus=name_rus,
                occupation=occupations,
                image_url=image_url
            )
        )
        print(data)
    return data


def parse_studio():
    data = []
    urls = anime_urls()
    for url in urls:
        print("studio", url)
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
        div_studio = soup.findAll("div", {"class": "block"})
        try:
            url = div_studio[5]("a")[0]["href"]
        except:
            url = None
        try:
            id = url.split("/")[-1].split("-")[0]
        except:
            id = None
        try:
            name = div_studio[5]("img")[0]["alt"]
        except:
            name =None
        try:
            image_url = div_studio[5]("img")[0]["src"]
        except:
            image_url = None
        data.append(
            Studio(
                url=url,
                id=id,
                name=name,
                image_url=image_url
            )
        )
    return data



if __name__ == "__main__":
    start_anime = parse_anime()
    print(start_anime)

