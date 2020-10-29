from dataclasses import dataclass


@dataclass
class PublishedTweet:
    id_: int
    tweet: str
    entity: object
