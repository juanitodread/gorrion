import re

from src.clients.spotify import Track
from src.templates.config import (
    TweetConfig,
    TweetBodyConfig,
    TweetFooterConfig,
)


class TweetTemplate:
    def __init__(self, track: Track, config: TweetConfig) -> None:
        self._track = track
        self._config = config

    def to_tweet(self) -> str:
        return (
            f'{self.header()}'
            f'{self.body()}'
            f'{self.footer()}'
        )

    def header(self) -> str:
        return 'Now listening 🔊🎶:\n\n' if self._config.with_header else ''

    def body(self) -> str:
        return f'{self._build_body()}\n' if self._config.with_body else ''

    def footer(self) -> str:
        return f'{self._build_footer()}' if self._config.with_footer else ''

    def _build_body(self) -> str:
        body = BodyTemplate(self._track, self._config.body_config)
        return body.to_body()

    def _build_footer(self) -> str:
        footer = FooterTemplate(self._track, self._config.footer_config)
        return footer.to_footer()


class BodyTemplate:
    def __init__(self, track: Track, config: TweetBodyConfig) -> None:
        self._track = track
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
        return (f'Track: {self._track.track_number}. {self._track.name}\n'
                if self._config.with_track else '')

    def album(self) -> str:
        return (f'Album: {self._track.album.name}\n'
                if self._config.with_album else '')

    def artists(self) -> str:
        if not self._config.with_artists:
            return ''

        artist_names = ', '.join([artist.name
                                  for artist in self._track.artists])
        return f'Artist: {artist_names}\n'

    def tracks(self) -> str:
        return (f'Tracks: {self._track.album.total_tracks}\n'
                if self._config.with_tracks else '')

    def release_date(self) -> str:
        if not self._config.with_release_date:
            return ''

        year = self._track.album.release_date.split('-')[0]
        return f'Release: {year}\n'


class FooterTemplate:
    def __init__(self, track: Track, config: TweetFooterConfig) -> None:
        self._track = track
        self._config = config

    def to_footer(self) -> str:
        return (
            f'{self.hashtags()}'
            f'{self.song_media_link()}'
            f'{self.album_media_link()}'
        )

    def hashtags(self) -> str:
        hashtags = (
            f'{self.gorrion_hashtags()}'
            f'{self.album_hashtags()}'
            f'{self.artists_hashtags()}'
        )
        return f'{hashtags.strip()}\n\n' if len(hashtags) > 0 else ''

    def gorrion_hashtags(self) -> str:
        return ('#gorrion #NowPlaying '
                if self._config.with_gorrion_hashtags else '')

    def album_hashtags(self) -> str:
        return (f'{self._build_hashtag(self._track.album.name)} '
                if self._config.with_album_hashtag else '')

    def artists_hashtags(self) -> str:
        if not self._config.with_artists_hashtag:
            return ''

        artists_hashtags = [self._build_hashtag(artist.name)
                            for artist in self._track.artists]
        return ' '.join(artists_hashtags)

    def song_media_link(self) -> str:
        return (f'{self._track.public_url}'
                if self._config.with_song_media_link else '')

    def album_media_link(self) -> str:
        return (f'{self._track.album.public_url}?si=g'
                if self._config.with_album_media_link else '')

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

        return f'#{hashtags}'
