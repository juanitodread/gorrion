from unittest.mock import patch, MagicMock

import pytest

from src.clients.twitter.client import Twitter, TwitterConfig
from src.clients.twitter.models import PublishedTweet


@pytest.fixture()
@patch('src.clients.twitter.client.tweepy.Client')
def twitter(tweepy_client_mock) -> Twitter:
    status = MagicMock()
    status.data = {'id': '123456'}
    tweepy_client_mock.return_value.create_tweet = MagicMock(return_value=status)

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
        assert twitter._client is not None

    def test_post(self, twitter):
        status = twitter.post('tweet status')

        assert status == PublishedTweet('123456', 'tweet status', None)

    def test_reply(self, twitter):
        status = twitter.reply('tweet status', '123456')

        assert status == PublishedTweet('123456', 'tweet status', None)

    def test_max_tweet_length(self, twitter):
        assert twitter.max_tweet_length == 280
