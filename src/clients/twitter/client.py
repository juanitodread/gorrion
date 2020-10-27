from tweepy import OAuthHandler, API, Status

from src.clients.twitter.config import TwitterConfig


class Twitter:
    def __init__(self, config: TwitterConfig) -> None:
        self._consumer_key = config.consumer_key
        self._consumer_secret = config.consumer_secret
        self._access_token = config.access_token
        self._access_token_secret = config.access_token_secret
        
        auth = OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)

        self._client = API(auth)

    def post(self, tweet: str) -> Status:
        status = self._client.update_status(tweet)

        return status

    def reply(self, tweet: str, tweet_id: int) -> Status:
        status = self._client.update_status(tweet, in_reply_to_status_id=tweet_id)

        return status

    @property
    def max_tweet_length(self) -> int:
        return 280
