from dataclasses import dataclass


@dataclass
class Entity:
    id_: str
    name: str
    href: str


@dataclass
class Album(Entity):
    release_date: str


@dataclass
class Artist(Entity):
    pass


@dataclass
class Track(Entity):
    track_number: int
    album: Album
    artists: list
