from dataclasses import dataclass


@dataclass
class Entity:
    id_: str
    name: str
    href: str
    public_url: str


@dataclass
class Artist(Entity):
    pass


@dataclass
class Track(Entity):
    disc_number: int
    track_number: int
    duration: int


@dataclass
class Album(Entity):
    release_date: str
    total_tracks: int
    artists: list
    tracks: list
