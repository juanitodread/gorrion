from dataclasses import dataclass


@dataclass
class SpotifyConfig:
    client_id: str
    client_secret: str
    refresh_token: str
