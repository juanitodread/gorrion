from unittest.mock import patch, MagicMock

import pytest

from src.clients.bluesky.client import Bluesky, BlueskyConfig
from src.clients.bluesky.models import PublishedPost


@pytest.fixture()
@patch('src.clients.bluesky.client.Client')
def bluesky(bluesky_client_mock) -> Bluesky:
    status = MagicMock()
    status.uri = 'cid-123'
    status.cid = 'http://uri.com'

    bluesky_client_mock.return_value.send_post = MagicMock(return_value=status)

    return Bluesky(BlueskyConfig(
        username='username',
        password='password',
    ))


class TestBluesky:
    def test_constructor(self, bluesky):
        assert bluesky._client is not None

    def test_post(self, bluesky):
        status = bluesky.post('tweet status')

        assert status == PublishedPost(
            cid='http://uri.com',
            uri='cid-123',
            post='tweet status',
            root_cid='http://uri.com',
            root_uri='cid-123',
            entity=None,
        )

    def test_reply(self, bluesky):
        root_post = PublishedPost(
            cid='http://uri-321.com',
            uri='cid-321',
            post='tweet status',
            root_cid='http://uri-321.com',
            root_uri='cid-321',
            entity=None,
        )

        status = bluesky.reply('reply status', root_post)

        assert status == PublishedPost(
            cid='http://uri.com',
            uri='cid-123',
            post='reply status',
            root_cid='http://uri-321.com',
            root_uri='cid-321',
            entity=None,
        )

    def test_max_post_length(self, bluesky):
        assert bluesky.max_post_length == 280
