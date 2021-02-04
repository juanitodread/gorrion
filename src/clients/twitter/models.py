from dataclasses import dataclass


@dataclass
class PublishedTweet:
    id_: str
    tweet: str
    entity: object
