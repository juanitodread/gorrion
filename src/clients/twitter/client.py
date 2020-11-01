import time

from tweepy import OAuthHandler, API

from src.clients.twitter.config import TwitterConfig
from src.clients.twitter.models import PublishedTweet


class Twitter:
    def __init__(self, config: TwitterConfig) -> None:
        self._consumer_key = config.consumer_key
        self._consumer_secret = config.consumer_secret
        self._access_token = config.access_token
        self._access_token_secret = config.access_token_secret
        self._retweet_delay = config.retweet_delay
        self._retweet_delay_secs = config.retweet_delay_secs
        
        auth = OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)

        self._client = API(auth)

    def post(self, tweet: str) -> PublishedTweet:
        status = self._client.update_status(tweet)

        return PublishedTweet(status.id, tweet, None)

    def reply(self, tweet: str, tweet_id: int) -> PublishedTweet:
        if self._retweet_delay:
            time.sleep(self._retweet_delay_secs)

        status = self._client.update_status(tweet, in_reply_to_status_id=tweet_id)

        return PublishedTweet(status.id, tweet, None)

    @property
    def max_tweet_length(self) -> int:
        return 280


class TwitterLocal(Twitter):
    def __init__(self, config: TwitterConfig) -> None:
        super().__init__(config)

    def post(self, tweet: str) -> PublishedTweet:
        return PublishedTweet('fake-status-id', tweet, None)

    def reply(self, tweet: str, tweet_id: int) -> PublishedTweet:
        if self._retweet_delay:
            time.sleep(self._retweet_delay_secs)
        return PublishedTweet('fake-status-id', tweet, None)
