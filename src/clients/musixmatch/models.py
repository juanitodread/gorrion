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
    tracks: list = None
    tracks_length: int = 0
    lyric: Lyric = None

    def __post_init__(self):
        self.name = self._sanitize(self.name, '(')
        self.name = self._sanitize(self.name, '-')

    def _sanitize(self, name: str, char_to_remove: str) -> str:
        found_char = name.find(char_to_remove)
        return name[0:found_char if found_char > 0 else len(name)].strip()
