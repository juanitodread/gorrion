import re

from atproto import client_utils
from atproto_client.utils import TextBuilder


from src.clients.spotify import Album
from src.templates.config import (
    TweetConfig,
    TweetBodyConfig,
    TweetFooterConfig,
)


class BlueskyTemplate:
    def __init__(self, album: Album, config: TweetConfig):
        self._album = album
        self._config = config
        self._text_builder = client_utils.TextBuilder()

    def to_tweet(self) -> TextBuilder:
        self.header()
        self.body()
        self.footer()

        return self._text_builder

    def to_text(self) -> str:
        return self._text_builder.build_text()

    def header(self) -> None:
        if not self._config.with_header:
            return None

        self._text_builder.text('Now listening 🔊🎶:\n\n')

    def body(self) -> None:
        if not self._config.with_body:
            return None

        self._text_builder.text(self._build_body())
        self._text_builder.text('\n')

    def footer(self) -> None:
        if not self._config.with_footer:
            return None

        self._build_footer(self._text_builder)

    def _build_body(self) -> str:
        body = BodyTemplate(self._album, self._config.body_config)
        return body.to_body()

    def _build_footer(self, text_builder: TextBuilder) -> None:
        footer = FooterTemplate(self._album, self._config.footer_config, text_builder)
        self._text_builder = footer.to_footer()


class BodyTemplate:
    def __init__(self, album: Album, config: TweetBodyConfig) -> None:
        self._album = album
        self._config = config

    def to_body(self) -> str:
        return (
            f'{self.track()}'
            f'{self.album()}'
            f'{self.artists()}'
            f'{self.tracks()}'
            f'{self.release_date()}'
        )

    def track(self) -> str:
        return (f'Track: {self._album.tracks[0].track_number}. {self._album.tracks[0].name}\n'
                if self._config.with_track else '')

    def album(self) -> str:
        return (f'Album: {self._album.name}\n'
                if self._config.with_album else '')

    def artists(self) -> str:
        if not self._config.with_artists:
            return ''

        artist_names = ', '.join([artist.name
                                  for artist in self._album.artists])
        return f'Artist: {artist_names}\n'

    def tracks(self) -> str:
        return (f'Tracks: {self._album.total_tracks}\n'
                if self._config.with_tracks else '')

    def release_date(self) -> str:
        if not self._config.with_release_date:
            return ''

        year = self._album.release_date.split('-')[0]
        return f'Release: {year}\n'


class FooterTemplate:
    def __init__(self, album: Album, config: TweetFooterConfig, text_builder: TextBuilder) -> None:
        self._album = album
        self._config = config
        self._text_builder = text_builder

    def to_footer(self) -> TextBuilder:
        self.hashtags()
        self.song_media_link()
        self.album_media_link()

        return self._text_builder

    def hashtags(self) -> None:
        self.gorrion_hashtags()
        self.album_hashtags()
        self.artists_hashtags()

        self._text_builder.text('\n\n')

    def gorrion_hashtags(self) -> None:
        if not self._config.with_gorrion_hashtags:
            return None

        self._text_builder.tag('#gorrion', 'gorrion')
        self._text_builder.text(' ')
        self._text_builder.tag('#NowPlaying', 'NowPlaying')
        self._text_builder.text(' ')

    def album_hashtags(self) -> None:
        if not self._config.with_album_hashtag:
            return None

        album_tag = self._build_hashtag(self._album.name)
        self._text_builder.tag(f'#{album_tag}', album_tag)
        self._text_builder.text(' ')

    def artists_hashtags(self) -> None:
        if not self._config.with_artists_hashtag:
            return None

        # Probably worth to investigate how to remove the remaining blank space.
        for artist in self._album.artists:
            artist_tag = self._build_hashtag(artist.name)
            self._text_builder.tag(f'#{artist_tag}', artist_tag)
            self._text_builder.text(' ')

    def song_media_link(self) -> None:
        if not self._config.with_song_media_link:
            return

        self._text_builder.link(self._album.tracks[0].public_url, self._album.tracks[0].public_url)

    def album_media_link(self) -> None:
        if not self._config.with_album_media_link:
            return

        link = f'{self._album.public_url}?si=g'
        self._text_builder.link(link, link)

    def _build_hashtag(self, text: str) -> str:
        if not text or len(text) == 0:
            return ''

        words = text.split(' ')

        hashtags = []
        for word in words:
            word = re.sub(r'\W+', '', word)
            word = (word.capitalize() if len(word) > 0 and word[0].islower()
                    else word)
            hashtags.append(word)

        hashtags = ''.join(hashtags)

        return hashtags
