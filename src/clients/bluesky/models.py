from dataclasses import dataclass


@dataclass
class BasePost:
    cid: str
    uri: str


@dataclass
class PublishedPost(BasePost):
    post: str
    root_cid: str
    root_uri: str
    entity: object
