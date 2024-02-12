from dataclasses import dataclass, field


@dataclass
class TweetBodyConfig:
    with_track: bool = False
    with_album: bool = False
    with_artists: bool = False
    with_tracks: bool = False
    with_release_date: bool = False


@dataclass
class TweetFooterConfig:
    with_gorrion_hashtags: bool = False
    with_album_hashtag: bool = False
    with_artists_hashtag: bool = False
    with_song_media_link: bool = False
    with_album_media_link: bool = False


@dataclass
class TweetConfig:
    with_header: bool = False
    with_body: bool = False
    with_footer: bool = False
    body_config: TweetBodyConfig = field(default_factory=TweetBodyConfig)
    footer_config: TweetFooterConfig = field(default_factory=TweetFooterConfig)


@dataclass
class TweetSongConfig(TweetConfig):
    with_header: bool = True
    with_body: bool = True
    with_footer: bool = True
    body_config: TweetBodyConfig = field(default_factory=lambda: TweetBodyConfig(
        with_track=True,
        with_album=True,
        with_artists=True,
        with_tracks=False,
        with_release_date=False,
    ))
    footer_config: TweetFooterConfig = field(default_factory=lambda: TweetFooterConfig(
        with_gorrion_hashtags=True,
        with_album_hashtag=False,
        with_artists_hashtag=True,
        with_song_media_link=True,
        with_album_media_link=False,
    ))


@dataclass
class TweetAlbumConfig(TweetConfig):
    with_header: bool = True
    with_body: bool = True
    with_footer: bool = True
    body_config: TweetBodyConfig = field(default_factory=lambda: TweetBodyConfig(
        with_track=False,
        with_album=True,
        with_artists=True,
        with_tracks=True,
        with_release_date=True,
    ))
    footer_config: TweetFooterConfig = field(default_factory=lambda: TweetFooterConfig(
        with_gorrion_hashtags=True,
        with_album_hashtag=True,
        with_artists_hashtag=True,
        with_song_media_link=False,
        with_album_media_link=True,
    ))
