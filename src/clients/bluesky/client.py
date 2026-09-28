import time

from atproto import Client, models

from src.clients.bluesky.config import BlueskyConfig
from src.clients.bluesky.models import BasePost, PublishedPost


class Bluesky:
    def __init__(self, config: BlueskyConfig) -> None:
        self.MAX_POST_LENGTH = 280
        self._replay_delay = config.replay_delay
        self._replay_delay_secs = config.replay_delay_secs

        self._client = Client()
        self._client.login(config.username, config.password)

        print('Bluesky Client created!')

    def post(self, text: str) -> PublishedPost:
        status = self._client.send_post(text=text)
        root = models.create_strong_ref(status)

        return PublishedPost(
            cid=status.cid,
            uri=status.uri,
            post=text,
            root_cid=root.cid,
            root_uri=root.uri,
            entity=None,
        )

    def reply(self, text: str, published_post: PublishedPost) -> PublishedPost:
        if self._replay_delay:
            time.sleep(self._replay_delay_secs)

        root = models.create_strong_ref(BasePost(cid=published_post.root_cid, uri=published_post.root_uri))
        previous_post = models.create_strong_ref(BasePost(cid=published_post.cid, uri=published_post.uri))

        status = self._client.send_post(
            text=text,
            reply_to=models.AppBskyFeedPost.ReplyRef(parent=previous_post, root=root),
        )
        return PublishedPost(
            cid=status.cid,
            uri=status.uri,
            post=text,
            root_cid=root.cid,
            root_uri=root.uri,
            entity=published_post.entity,
        )

    @property
    def max_post_length(self) -> int:
        return self.MAX_POST_LENGTH


class BlueskyLocal(Bluesky):
    def __init__(self, config: BlueskyConfig) -> None:
        self.MAX_POST_LENGTH = 280
        self._replay_delay = config.replay_delay
        self._replay_delay_secs = config.replay_delay_secs

        self._client = None

        print('Bluesky Mock-Client created!')

    def post(self, text: str) -> PublishedPost:
        return PublishedPost(
            cid='cid-123',
            uri='uri-123',
            post=text,
            root_cid='root-cid-123',
            root_uri='root-uri-123',
            entity=None,
        )

    def reply(self, text: str, published_post: PublishedPost) -> PublishedPost:
        if self._replay_delay:
            time.sleep(self._replay_delay_secs)

        return self.post(text)


class BlueskyFactory:
    @staticmethod
    def get_client(config: BlueskyConfig) -> Bluesky:
        if config.use_mock:
            return BlueskyLocal(config)
        else:
            return Bluesky(config)
