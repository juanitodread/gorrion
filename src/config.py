import os

from src.clients.spotify import SpotifyConfig
from src.clients.twitter import TwitterConfig
from src.clients.bluesky import BlueskyConfig
from src.clients.musixmatch import MusixmatchConfig


class Config:
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')

    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_CONFIG_RETWEET_DELAY = os.getenv('TWITTER_CONFIG_RETWEET_DELAY', 'True') == 'True'
    TWITTER_CONFIG_RETWEET_DELAY_SECS = int(os.getenv('TWITTER_CONFIG_RETWEET_DELAY_SECS', 3))
    TWITTER_CONFIG_USE_MOCK = os.getenv('TWITTER_CONFIG_USE_MOCK', 'True') == 'True'

    BLUESKY_USERNAME = os.getenv('BLUESKY_USERNAME')
    BLUESKY_APP_PASSWORD = os.getenv('BLUESKY_APP_PASSWORD')
    BLUESKY_CONFIG_REPLAY_DELAY = os.getenv('BLUESKY_CONFIG_REPLAY_DELAY', 'True') == 'True'
    BLUESKY_CONFIG_REPLAY_DELAY_SECS = int(os.getenv('BLUESKY_CONFIG_REPLAY_DELAY_SECS', 10))
    BLUESKY_CONFIG_USE_MOCK = os.getenv('BLUESKY_CONFIG_USE_MOCK', 'True') == 'True'

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
            Config.TWITTER_CONFIG_USE_MOCK,
        )

    @staticmethod
    def get_bluesky_config() -> BlueskyConfig:
        return BlueskyConfig(
            Config.BLUESKY_USERNAME,
            Config.BLUESKY_APP_PASSWORD,
            Config.BLUESKY_CONFIG_REPLAY_DELAY,
            Config.BLUESKY_CONFIG_REPLAY_DELAY_SECS,
            Config.BLUESKY_CONFIG_USE_MOCK,
        )

    @staticmethod
    def get_musixmatch_config() -> MusixmatchConfig:
        return MusixmatchConfig(
            Config.MUSIXMATCH_API_KEY,
        )
