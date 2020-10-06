from unittest.mock import patch, MagicMock

from src.clients.twitter.client import Twitter


class TestTwitter:
    @patch('src.clients.twitter.client.API')
    def test_constructor(self, API_mock):
        twitter = Twitter(
            'consumer-key',
            'consumer-secret',
            'access-token',
            'access-token-secret',
        )

        assert twitter._consumer_key == 'consumer-key'
        assert twitter._consumer_secret == 'consumer-secret'
        assert twitter._access_token == 'access-token'
        assert twitter._access_token_secret == 'access-token-secret'
        assert twitter._client != None

    def test_max_tweet_length(self):
        twitter = Twitter(
            'consumer-key',
            'consumer-secret',
            'access-token',
            'access-token-secret',
        )

        assert twitter.max_tweet_length == 280

    @patch('src.clients.twitter.client.API')
    def test_post(self, API_mock):
        API_mock.return_value.update_status = MagicMock(return_value='Tweet ha sido enviado')

        twitter = Twitter(
            'consumer-key',
            'consumer-secret',
            'access-token',
            'access-token-secret',
        )

        status = twitter.post('tweet status')

        assert status == 'Tweet ha sido enviado'
