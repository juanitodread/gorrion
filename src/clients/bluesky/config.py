from dataclasses import dataclass


@dataclass
class BlueskyConfig:
    username: str
    password: str
    replay_delay: bool = False
    replay_delay_secs: int = 3
    use_mock: bool = True
