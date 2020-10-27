from dataclasses import dataclass


@dataclass
class TwitterConfig:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
