from unittest.mock import patch, MagicMock

import pytest

from src.clients.twitter.client import Twitter, TwitterConfig


@pytest.fixture()
@patch('src.clients.twitter.client.API')
def twitter(API_mock) -> Twitter:
    API_mock.return_value.update_status = MagicMock(return_value='Tweet has been sent')

    return Twitter(TwitterConfig(
        'consumer-key',
        'consumer-secret',
        'access-token',
        'access-token-secret',
    ))


class TestTwitter:
    def test_constructor(self, twitter):
        assert twitter._consumer_key == 'consumer-key'
        assert twitter._consumer_secret == 'consumer-secret'
        assert twitter._access_token == 'access-token'
        assert twitter._access_token_secret == 'access-token-secret'
        assert twitter._client != None

    def test_max_tweet_length(self, twitter):
        assert twitter.max_tweet_length == 280

    def test_post(self, twitter):
        status = twitter.post('tweet status')

        assert status == 'Tweet has been sent'

    def test_reply(self, twitter):
        status = twitter.reply('tweet status', '12345')

        assert status == 'Tweet has been sent'
