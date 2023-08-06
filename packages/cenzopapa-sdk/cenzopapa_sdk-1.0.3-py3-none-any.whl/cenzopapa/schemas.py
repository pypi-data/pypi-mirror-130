import datetime
from dataclasses import dataclass


@dataclass
class Image:
    id: int
    url: str
    width: int
    height: 313
    posted_at: datetime.datetime
    author: int
    likes: list
    likes_count: int


@dataclass
class ImageList:
    count: int
    next: str
    previous: str
    results: list[Image]
