import os

from src.clients.spotify import SpotifyConfig
from src.clients.twitter import TwitterConfig
from src.clients.musixmatch import MusixmatchConfig


class Config:
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')

    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_CONFIG_RETWEET_DELAY = os.getenv('TWITTER_CONFIG_RETWEET_DELAY') == 'True'
    TWITTER_CONFIG_RETWEET_DELAY_SECS = int(os.getenv('TWITTER_CONFIG_RETWEET_DELAY_SECS', 3))

    MUSIXMATCH_API_KEY = os.getenv('MUSIXMATCH_API_KEY')

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_OWNER_USERNAME = os.getenv('TELEGRAM_OWNER_USERNAME')

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
            Config.TWITTER_CONFIG_RETWEET_DELAY,
            Config.TWITTER_CONFIG_RETWEET_DELAY_SECS,
        )

    @staticmethod
    def get_musixmatch_config() -> MusixmatchConfig:
        return MusixmatchConfig(
            Config.MUSIXMATCH_API_KEY,
        )
