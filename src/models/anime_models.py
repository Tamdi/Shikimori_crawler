from pydantic import BaseModel
from typing import Optional, List


class Character(BaseModel):
    url: str
    id: List[str]
    name: List[str]
    name_rus: List[str]
    image_url: List[str]


class Staff(BaseModel):
    url: str
    id: List[str]
    name: List[str]
    name_rus: List[str]
    occupation: List[str]
    image_url: List[str]


class Studio(BaseModel):
    url: str
    id: str
    name: str
    image_url: str


class Anime(BaseModel):
    url: str
    id: str
    name: str
    name_rus: str
    name_alt: str
    type: str
    total_episodes: int
    current_episodes: str
    next_episode_date: str
    started: str
    genres: Optional[str]
    score: float
    rating: str
    licensed_by: str
    studio: List[Studio]
    description: str
    related: Optional[List[str]]
    author: Optional[List[Staff]]
    main_heroes: Optional[List[Character]]
    scenes: Optional[List[str]]
    videos: Optional[List[str]]
    similar: Optional[List[str]]
    image_url: str

