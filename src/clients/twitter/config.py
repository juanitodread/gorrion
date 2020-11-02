from dataclasses import dataclass


@dataclass
class TwitterConfig:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
    retweet_delay: bool = False
    retweet_delay_secs: int = 3
