from dataclasses import dataclass


@dataclass
class Entity:
    id_: str
    name: str
    href: str
    public_url: str


@dataclass
class Album(Entity):
    release_date: str
    total_tracks: int
    artists: list
    tracks: list


@dataclass
class Artist(Entity):
    pass


@dataclass
class Track(Entity):
    track_number: int
