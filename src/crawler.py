import time
import requests
import logging
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
            soup = BeautifulSoup(response.json()["content"], "html.parser")
            urls = soup.findAll("a", {"class": "cover anime-tooltip"})
            for new in urls:
                url = new["href"]
                url_list.append(url)
    return url_list


def p_characters(url):
    data = []
    id = []
    name = []
    name_rus = []
    image_url = []
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
            # print("Could not get response (p_characters) for url:", url)
            logging.error('TypeError. Could not get response (p_characters) for url:', url)
            return data
            # raise Exception("Could not get url's response (p_characters)")
    resources_url = url + "/resources"
    response_resources_url = requests.get(
        resources_url,
        headers=headers,
        timeout=10
    )
    soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")

    try:
        div_character = soup_resources.find("div", {"class": "cc-characters"}).find("div", {"class":
                                                                                                "cc m0 to-process"})
        if div_character.find("span", {"class": "name-en"}):
            div_name = div_character.findAll("span", {"class": "name-en"})
        else:
            div_name = []
        if div_character.find("span", {"class": "name-ru"}):
            div_name_rus = div_character.findAll("span", {"class": "name-ru"})
        else:
            div_name_rus = []
        if div_character.find("span", {"class": "image-cutter"}):
            div_image_url = div_character.findAll("span", {"class": "image-cutter"})
        else:
            div_image_url = []
    except AttributeError:
        logging.error(
            "AttributeError: 'NoneType' object has no attribute 'text' (p_characters: div_authors) in url:", url)
        div_character = []
        div_name = []
        div_name_rus = []
        div_image_url = []

    for i in div_character:
        id.append(i["id"])
    for i in div_name:
        name.append(i.text)
    for i in div_name_rus:
        name_rus.append(i.text)
    for i in div_image_url:
        image_url.append(i("img")[0]["src"])
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


def p_staff(url):
    data = []
    id = []
    name = []
    name_rus = []
    occupations = []
    image_url = []
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
            logging.error("TypeError. Could not get response (p_staff) for url: ", url)
            return data
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
    except AttributeError:
        logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_authors) in url:", url)
        div_id = []
    try:
        div_name = div_authors.findAll("span", {"class": "name-en"})
    except AttributeError:
        logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_name) in url:", url)
        div_name = []
    try:
        div_name_rus = div_authors.findAll("span", {"class": "name-ru"})
    except AttributeError:
        logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_name_rus) in url:", url)
        div_name_rus = []
    try:
        div_image_url = div_authors.findAll("div", {"class": "image linkeable bubbled"})
    except AttributeError:
        logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_image_url) in url:", url)
        div_image_url = []

    for i in div_id:
        id.append(i["data-id"])
    for i in div_name:
        name.append(i.text)
    for i in div_name_rus:
        name_rus.append(i.text)
    for author_div in soup_resources.find_all("div", {"class": "b-db_entry-variant-list_item", "data-type": "person"}):
        a = [btag.text for btag in author_div.find_all("div", {"class": "b-tag"}) if len(btag["class"]) == 1]
        occupations.append(", ".join(a))
    for i in div_image_url:
        image_url.append(i("img")[0]["src"])

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
    return data


def p_studio(url):
    data = []
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
            logging.error("Could not get response (p_studio) for url: ", url)
            return data

    soup = BeautifulSoup(response_url.text, "html.parser")
    div_studio = soup.findAll("div", {"class": "block"})
    try:
        url = div_studio[5]("a")[0]["href"]
        id = url.split("/")[-1].split("-")[0]
    except IndexError:
        logging.error("IndexError: list index out of range (p_studio: url, id) in url:", url)
        url = ""
        id = ""
    try:
        name = div_studio[5]("img")[0]["alt"]
    except IndexError:
        logging.error("IndexError: list index out of range (p_studio: name) in url:", url)
        name = ""
    try:
        image_url = div_studio[5]("img")[0]["src"]
    except IndexError:
        logging.error("IndexError: list index out of range (p_studio: image_url) in url:", url)
        image_url = ""

    data.append(
        Studio(
            url=url,
            id=id,
            name=name,
            image_url=image_url
        )
    )
    return data


def parse_anime():
    data = []
    urls = anime_urls()
    for url in urls:
        related = []
        scenes = []
        videos = []
        similar = []
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
                logging.error("Could not get response (parse_anime) for url:", url)
                continue

        soup = BeautifulSoup(response_url.text, "html.parser")
        id = url.split("/")[-1].split("-")[0]
        div_name = soup.find("header", {"class": "head"})
        name = div_name('meta')[0]["content"]
        div_image = soup.find("div", {"class": "c-poster"})
        image_url = div_image('img')[0]["src"]
        div = soup.findAll("div", {"class": "value"})
        type = div[0].text.strip() if div[0].text.strip() else None
        current_episodes = div[1].text.strip().split(" /")[0] if div[1].text.strip().split(" /")[0] else None
        try:
            total_episodes = div[1].text.strip().split(" /")[1]
        except IndexError:
            logging.error("IndexError: list index out of range (parse_anime: total_episodes) in url:", url)
            total_episodes = ""
        next_episode_date = div[2].text.strip() if div[2].text.strip() else None
        started = div[4].text.strip() if div[4].text.strip() else None
        genres = ""
        if div[5].find("span", {"class": "genre-ru"}):
            genre_ru = div[5].findAll("span", {"class": "genre-ru"})
            for i in genre_ru:
                genres = i.text + "; " + genres
        else:
            if div[4].find("span", {"class": "genre-ru"}):
                genre_ru = div[4].findAll("span", {"class": "genre-ru"})
                for i in genre_ru:
                    genres = i.text + "; " + genres
            else:
                if div[3].find("span", {"class": "genre-ru"}):
                    genre_ru = div[3].findAll("span", {"class": "genre-ru"})
                    for i in genre_ru:
                        genres = i.text + "; " + genres
                else:
                    genres = ""
        try:
            rating = div[6].text.strip()
        except IndexError:
            logging.error("IndexError: list index out of range (parse_anime: rating) in url:", url)
            rating = ""
        try:
            licensed_by = div[7].text.strip()
        except IndexError:
            logging.error("IndexError: list index out of range (parse_anime: licensed_by) in url:", url)
            licensed_by = ""

        div_name_rus = soup.find("header", {"class": "head"})
        if div_name_rus.find('h1') is not None:
            name_rus = div_name_rus.find('h1').text.strip().split(" /")[0]
        else:
            name_rus = ""

        div_rating = soup.find("div", {"class": "score-value score-9"})
        try:
            score = div_rating.text.strip()
        except AttributeError:
            logging.error("AttributeError: 'NoneType' object has no attribute 'text' (parse_anime: score) in url:", url)
            score = ""

        div_description = soup.find("div", {"class": "b-text_with_paragraphs"})
        try:
            description = div_description.text.strip()
        except AttributeError:
            logging.error(
                "AttributeError: 'NoneType' object has no attribute 'text' (parse_anime: description) in url: ", url)
            description = ""

        resources_url = url + "/resources"
        response_resources_url = requests.get(
            resources_url,
            headers=headers,
            timeout=10
        )
        soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")
        try:
            div_related = soup_resources.find("div", class_="c-column block_m").findAll(class_=
                                                                                        "b-db_entry-variant-list_item")
        except AttributeError:
            logging.error(
                "AttributeError: 'NoneType' object has no attribute 'text' (parse_anime: div_image_url) in url:", url)
            div_related = []
        try:
            div_scenes = soup_resources.find("div", class_="c-screenshots").find(class_="cc")
        except AttributeError:
            logging.error(
                "AttributeError: 'NoneType' object has no attribute 'text' (parse_anime: div_image_url) in url:", url)
            div_scenes = []
        try:
            div_videos = soup_resources.find("div", class_="c-videos").find(class_="cc").findAll(class_="video-link")
        except AttributeError:
            logging.error(
                "AttributeError: 'NoneType' object has no attribute 'text' (parse_anime: div_image_url) in url:", url)
            div_videos = []
        try:
            div_similar = soup_resources.find("div", class_="cc cc-similar to-process").findAll(class_="title two_lined")
        except AttributeError:
            logging.error(
                "AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_image_url) in url:", url)
            div_similar = []

        for i in div_related:
            related.append(i["data-url"])
        for i in div_scenes:
            scenes.append(i["href"])
        for i in div_videos:
            videos.append(i["href"])
        for i in div_similar:
            similar.append(i["href"])

        div_other_names = soup.find(
            "span", {"class": "other-names"}) if soup.find("span", {"class": "other-names"}) else None
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
        except IndexError:
            logging.error("IndexError: list index out of range (parse_anime: name_alt) in url:", url)
            name_alt = ""

        studio: list[Studio]
        author: list[Staff]
        main_heroes: list[Character]
        author = p_staff(url)
        studio = p_studio(url)
        main_heroes = p_characters(url)

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
                # print("Could not get response (p_characters) for url:", url)
                logging.error('TypeError. Could not get response (p_characters) for url:', url)
                return data
                # raise Exception("Could not get url's response (p_characters)")
        resources_url = url + "/resources"
        response_resources_url = requests.get(
            resources_url,
            headers=headers,
            timeout=10
        )
        soup_resources = BeautifulSoup(response_resources_url.text, "html.parser")

        try:
            div_character = soup_resources.find("div", {"class": "cc-characters"}).find("div", {"class":
                                                                                                    "cc m0 to-process"})
            if div_character.find("span", {"class": "name-en"}):
                div_name = div_character.findAll("span", {"class": "name-en"})
            else:
                div_name = []
            if div_character.find("span", {"class": "name-ru"}):
                div_name_rus = div_character.findAll("span", {"class": "name-ru"})
            else:
                div_name_rus = []
            if div_character.find("span", {"class": "image-cutter"}):
                div_image_url = div_character.findAll("span", {"class": "image-cutter"})
            else:
                div_image_url = []
        except AttributeError:
            logging.error(
                "AttributeError: 'NoneType' object has no attribute 'text' (p_characters: div_authors) in url:", url)
            div_character = []
            div_name = []
            div_name_rus = []
            div_image_url = []

        for i in div_character:
            id.append(i["id"])
        for i in div_name:
            name.append(i.text)
        for i in div_name_rus:
            name_rus.append(i.text)
        for i in div_image_url:
            image_url.append(i("img")[0]["src"])
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
                logging.error("TypeError. Could not get response (p_staff) for url: ", url)
                return data
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
        except AttributeError:
            logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_authors) in url:",
                          url)
            div_id = []
        try:
            div_name = div_authors.findAll("span", {"class": "name-en"})
        except AttributeError:
            logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_name) in url:", url)
            div_name = []
        try:
            div_name_rus = div_authors.findAll("span", {"class": "name-ru"})
        except AttributeError:
            logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_name_rus) in url:",
                          url)
            div_name_rus = []
        try:
            div_image_url = div_authors.findAll("div", {"class": "image linkeable bubbled"})
        except AttributeError:
            logging.error("AttributeError: 'NoneType' object has no attribute 'text' (p_staff: div_image_url) in url:",
                          url)
            div_image_url = []

        for i in div_id:
            id.append(i["data-id"])
        for i in div_name:
            name.append(i.text)
        for i in div_name_rus:
            name_rus.append(i.text)
        for author_div in soup_resources.find_all("div",
                                                  {"class": "b-db_entry-variant-list_item", "data-type": "person"}):
            a = [btag.text for btag in author_div.find_all("div", {"class": "b-tag"}) if len(btag["class"]) == 1]
            occupations.append(", ".join(a))
        for i in div_image_url:
            image_url.append(i("img")[0]["src"])

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
    return data


def parse_studio():
    data = []
    urls = anime_urls()
    for url in urls:
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
                logging.error("Could not get response (p_studio) for url: ", url)
                return data

        soup = BeautifulSoup(response_url.text, "html.parser")
        div_studio = soup.findAll("div", {"class": "block"})
        try:
            url = div_studio[5]("a")[0]["href"]
            id = url.split("/")[-1].split("-")[0]
        except IndexError:
            logging.error("IndexError: list index out of range (p_studio: url, id) in url:", url)
            url = ""
            id = ""
        try:
            name = div_studio[5]("img")[0]["alt"]
        except IndexError:
            logging.error("IndexError: list index out of range (p_studio: name) in url:", url)
            name = ""
        try:
            image_url = div_studio[5]("img")[0]["src"]
        except IndexError:
            logging.error("IndexError: list index out of range (p_studio: image_url) in url:", url)
            image_url = ""

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
