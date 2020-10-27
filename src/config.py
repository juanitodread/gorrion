from src.clients.spotify import SpotifyConfig
from src.clients.twitter import TwitterConfig
from src.clients.musixmatch import MusixmatchConfig


class Config:
    SPOTIFY_CLIENT_ID = ''
    SPOTIFY_CLIENT_SECRET = ''
    SPOTIFY_REFRESH_TOKEN = ''

    TWITTER_CONSUMER_KEY = ''
    TWITTER_CONSUMER_SECRET = ''
    TWITTER_ACCESS_TOKEN = ''
    TWITTER_ACCESS_TOKEN_SECRET = ''

    MUSIXMATCH_API_KEY = ''

    @staticmethod
    def get_spotify_config() -> SpotifyConfig:
        return SpotifyConfig(
            Config.SPOTIFY_CLIENT_ID,
            Config.SPOTIFY_CLIENT_SECRET,
            Config.SPOTIFY_REFRESH_TOKEN,
        )

    @staticmethod
    def get_twitter_config() -> TwitterConfig:
        return TwitterConfig(
            Config.TWITTER_CONSUMER_KEY,
            Config.TWITTER_CONSUMER_SECRET,
            Config.TWITTER_ACCESS_TOKEN,
            Config.TWITTER_ACCESS_TOKEN_SECRET,
        )

    @staticmethod
    def get_musixmatch_config() -> MusixmatchConfig:
        return MusixmatchConfig(
            Config.MUSIXMATCH_API_KEY,
        )
