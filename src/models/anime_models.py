from pydantic import BaseModel
from typing import Optional, List


class Character(BaseModel):
    url: str
    id: Optional[List[str]]
    name: Optional[List[str]]
    name_rus: Optional[List[str]]
    image_url: Optional[List[str]]


class Staff(BaseModel):
    url: str
    id: List[str]
    name: Optional[List[str]]
    name_rus: Optional[List[str]]
    occupation: Optional[List[str]]
    image_url: Optional[List[str]]


class Studio(BaseModel):
    url: str
    id: str
    name: Optional[str]
    image_url: Optional[str]


class Anime(BaseModel):
    url: str
    id: str
    name: str
    name_rus: Optional[str]
    name_alt: Optional[str]
    type: Optional[str]
    total_episodes: Optional[int]
    current_episodes: Optional[str]
    next_episode_date: Optional[str]
    started: Optional[str]
    genres: Optional[str]
    score: Optional[float]
    rating: Optional[str]
    licensed_by: Optional[str]
    studio: Optional[List[Studio]]
    description: Optional[str]
    related: Optional[List[str]]
    author: Optional[List[Staff]]
    main_heroes: Optional[List[Character]]
    scenes: Optional[List[str]]
    videos: Optional[List[str]]
    similar: Optional[List[str]]
    image_url: str

