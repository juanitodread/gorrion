from dataclasses import dataclass, field


@dataclass
class TweetBodyConfig:
    with_track: bool
    with_album: bool
    with_artists: bool
    with_tracks: bool
    with_release_date: bool


@dataclass
class TweetFooterConfig:
    with_gorrion_hashtags: bool
    with_album_hashtag: bool
    with_artists_hashtag: bool
    with_song_media_link: bool
    with_album_media_link: bool


@dataclass
class TweetConfig:
    with_header: bool = field(init=False, default=False)
    with_body: bool = field(init=False, default=False)
    with_footer: bool = field(init=False, default=False)
    body_config: TweetBodyConfig = field(
        init=False,
        default=TweetBodyConfig(
            with_track=False,
            with_album=False,
            with_artists=False,
            with_tracks=False,
            with_release_date=False,
        )
    )
    footer_config: TweetFooterConfig = field(
        init=False,
        default=TweetFooterConfig(
            with_gorrion_hashtags=False,
            with_album_hashtag=False,
            with_artists_hashtag=False,
            with_song_media_link=False,
            with_album_media_link=False,
        )
    )


@dataclass
class TweetSongConfig(TweetConfig):
    with_header = True
    with_body = True
    with_footer = True
    body_config = TweetBodyConfig(
        with_track=True,
        with_album=True,
        with_artists=True,
        with_tracks=False,
        with_release_date=False,
    )
    footer_config = TweetFooterConfig(
        with_gorrion_hashtags=True,
        with_album_hashtag=False,
        with_artists_hashtag=True,
        with_song_media_link=True,
        with_album_media_link=False,
    )


@dataclass
class TweetAlbumConfig(TweetConfig):
    with_header = True
    with_body = True
    with_footer = True
    body_config = TweetBodyConfig(
        with_track=False,
        with_album=True,
        with_artists=True,
        with_tracks=True,
        with_release_date=True,
    )
    footer_config = TweetFooterConfig(
        with_gorrion_hashtags=True,
        with_album_hashtag=True,
        with_artists_hashtag=True,
        with_song_media_link=False,
        with_album_media_link=True,
    )
