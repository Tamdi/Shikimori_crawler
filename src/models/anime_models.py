from pydantic import BaseModel
from typing import Optional


class Anime(BaseModel):
    url: str
    id: int
    name: str
    name_rus: Optional[str]
    name_alt: Optional[str]
    type: Optional[str]
    total_episodes: Optional[int]  # ONA OVA
    current_episodes: Optional[int]
    next_episode_date: Optional[str]
    started: Optional[str]
    genres: Optional[str]
    score: Optional[float]
    rating: Optional[str]
    licensed_by: Optional[str]
    studio: Optional[str]
    description: Optional[str]
    related: Optional[str]
    author: Optional[str]
    main_heroes: Optional[str]
    secondary_heroes: Optional[str]
    scenes: Optional[str]
    videos: Optional[str]
    similar: Optional[str]
    image_url: str


class Character(BaseModel):
    url: str
    id: int
    name: str
    name_rus: str
    seiyu: str
    description: str
    image_url: str


class Staff(BaseModel):
    url: str
    id: int
    name: str
    name_rus: str
    birth_date: Optional[str]
    occupation: str
    description: Optional[str]
    titles: str
    characters: str
    image_url: str


class Studio(BaseModel):
    url: str
    id: int
    name: str
    image_url: str

