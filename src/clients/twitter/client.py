from tweepy import OAuthHandler, API


class Twitter:
    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token: str,
                 access_token_secret: str) -> None:
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        
        auth = OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)

        self._client = API(auth)

    def post(self, tweet: str):
        status = self._client.update_status(tweet)

        return status

    @property
    def max_tweet_length(self) -> int:
        return 280
