from dataclasses import dataclass


@dataclass
class Lyric:
    id_: str
    track_id: str
    common_track_id: str
    content: list


@dataclass
class Track:
    id_: str
    common_id: str
    name: str
    instrumental: int
    explicit: int
    artist: str
    album: str


@dataclass
class Song:
    name: str
    artist: str
    album: str
    tracks: list=None
    tracks_length: int=0
    lyric: Lyric=None

    def __post_init__(self):
        has_parentheses = self.name.find('(')
        self.name = self.name[0:has_parentheses if has_parentheses > 0 else len(self.name)].strip()
