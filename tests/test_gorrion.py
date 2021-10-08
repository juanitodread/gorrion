from unittest.mock import MagicMock

import pytest

from src.gorrion import Gorrion
from src.config import Config
from src.clients.spotify import (
    Track,
    Album,
    Artist
)
from src.clients.musixmatch import Song, Lyric
from src.clients.twitter import TwitterLocal, PublishedTweet
from src.templates import TweetSongConfig, TweetAlbumConfig


@pytest.fixture()
def twitter():
    return TwitterLocal(Config.get_twitter_config())


@pytest.fixture()
def track():
    return Album(
        id_='11',
        name='Pa morirse de amor',
        href='',
        public_url='http://spotify.com/album/11',
        release_date='2006-01-01',
        total_tracks=19,
        artists=[
            Artist(
                id_='12',
                name='Ely Guerra',
                href='',
                public_url='http://spotify.com/artist/12',
            )
        ],
        tracks=[
            Track(
                id_='1',
                name='Peligro',
                href='',
                public_url='http://spotify.com/track/1',
                disc_number=1,
                track_number=1,
                duration=1000,
            )
        ],
    )


@pytest.fixture()
def lyric():
    return Lyric('123', '456', '789', ['lyric1', 'lyric2'])


@pytest.fixture()
def song():
    return Song('Peligro', 'Ely Guerra', 'Pa morirse de amor')


class TestGorrion:
    def test_constructor(self, twitter):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        assert gorrion._spotify is not None
        assert gorrion._twitter is not None
        assert gorrion._musixmatch is not None

    def test_playing(self, twitter, track, song, lyric):
        spotify_mock = MagicMock()
        spotify_mock.get_current_track.return_value = track

        musixmatch_mock = MagicMock()
        song.lyric = lyric
        musixmatch_mock.fetch_lyric.return_value = song

        gorrion = Gorrion(spotify_mock, twitter, musixmatch_mock)
        tweet = gorrion.playing()

        assert tweet == PublishedTweet(
            id_='fake-status-id',
            tweet=(
                'Now listening 🔊🎶:\n\n'
                'Track: 1. Peligro\n'
                'Album: Pa morirse de amor\n'
                'Artist: Ely Guerra\n\n'
                '#gorrion #NowPlaying #ElyGuerra\n\n'
                'http://spotify.com/track/1'
            ),
            entity=Album(
                id_='11',
                name='Pa morirse de amor',
                href='',
                public_url='http://spotify.com/album/11',
                release_date='2006-01-01',
                total_tracks=19,
                artists=[
                    Artist(
                        id_='12',
                        name='Ely Guerra',
                        href='',
                        public_url='http://spotify.com/artist/12',
                    )
                ],
                tracks=[
                    Track(
                        id_='1',
                        name='Peligro',
                        href='',
                        public_url='http://spotify.com/track/1',
                        disc_number=1,
                        track_number=1,
                        duration=1000,
                    )
                ],
            )
        )

    def test_playing_with_lyric(self, twitter, track, song, lyric):
        spotify_mock = MagicMock()
        spotify_mock.get_current_track.return_value = track

        musixmatch_mock = MagicMock()
        song.lyric = lyric
        musixmatch_mock.fetch_lyric.return_value = song

        gorrion = Gorrion(spotify_mock, twitter, musixmatch_mock)
        tweets = gorrion.playing_with_lyrics()

        assert tweets == [
            PublishedTweet(
                id_='fake-status-id',
                tweet=(
                    'Now listening 🔊🎶:\n\n'
                    'Track: 1. Peligro\n'
                    'Album: Pa morirse de amor\n'
                    'Artist: Ely Guerra\n\n'
                    '#gorrion #NowPlaying #ElyGuerra\n\n'
                    'http://spotify.com/track/1'
                ),
                entity=Album(
                    id_='11',
                    name='Pa morirse de amor',
                    href='',
                    public_url='http://spotify.com/album/11',
                    release_date='2006-01-01',
                    total_tracks=19,
                    artists=[
                        Artist(
                            id_='12',
                            name='Ely Guerra',
                            href='',
                            public_url='http://spotify.com/artist/12',
                        )
                    ],
                    tracks=[
                        Track(
                            id_='1',
                            name='Peligro',
                            href='',
                            public_url='http://spotify.com/track/1',
                            disc_number=1,
                            track_number=1,
                            duration=1000,
                        )
                    ],
                )
            ),
            PublishedTweet(id_='fake-status-id', tweet='lyric1', entity=None),
            PublishedTweet(id_='fake-status-id', tweet='lyric2', entity=None),
        ]

    def test_playing_album(self, twitter, track, song, lyric):
        spotify_mock = MagicMock()
        spotify_mock.get_current_track.return_value = track

        musixmatch_mock = MagicMock()
        song.lyric = lyric
        musixmatch_mock.fetch_lyric.return_value = song

        gorrion = Gorrion(spotify_mock, twitter, musixmatch_mock)
        tweet = gorrion.playing_album()

        assert tweet == PublishedTweet(
            id_='fake-status-id',
            tweet=(
                'Now listening 🔊🎶:\n\n'
                'Album: Pa morirse de amor\n'
                'Artist: Ely Guerra\n'
                'Tracks: 19\n'
                'Release: 2006\n\n'
                '#gorrion #NowPlaying #PaMorirseDeAmor #ElyGuerra\n\n'
                'http://spotify.com/album/11?si=g'
            ),
            entity=Album(
                id_='11',
                name='Pa morirse de amor',
                href='',
                public_url='http://spotify.com/album/11',
                release_date='2006-01-01',
                total_tracks=19,
                artists=[
                    Artist(
                        id_='12',
                        name='Ely Guerra',
                        href='',
                        public_url='http://spotify.com/artist/12',
                    )
                ],
                tracks=[
                    Track(
                        id_='1',
                        name='Peligro',
                        href='',
                        public_url='http://spotify.com/track/1',
                        disc_number=1,
                        track_number=1,
                        duration=1000,
                    )
                ],
            )
        )

    def test_get_playing_album(self, twitter, track):
        spotify_mock = MagicMock()
        spotify_mock.get_current_track.return_value = track

        gorrion = Gorrion(spotify_mock, twitter, MagicMock())

        current_album = gorrion.get_playing_album()

        assert current_album == Album(
            id_='11',
            name='Pa morirse de amor',
            href='',
            public_url='http://spotify.com/album/11',
            release_date='2006-01-01',
            total_tracks=19,
            artists=[
                Artist(
                    id_='12',
                    name='Ely Guerra',
                    href='',
                    public_url='http://spotify.com/artist/12',
                )
            ],
            tracks=[
                Track(
                    id_='1',
                    name='Peligro',
                    href='',
                    public_url='http://spotify.com/track/1',
                    disc_number=1,
                    track_number=1,
                    duration=1000,
                )
            ],
        )

    def test_get_lyric(self, twitter, track, song, lyric):
        musixmatch_mock = MagicMock()
        musixmatch_mock.search_song.return_value = song
        song.lyric = lyric
        musixmatch_mock.fetch_lyric.return_value = song

        gorrion = Gorrion(MagicMock(), twitter, musixmatch_mock)

        song = gorrion.get_lyric(track)

        assert song == Song(
            name='Peligro',
            artist='Ely Guerra',
            album='Pa morirse de amor',
            tracks=None,
            tracks_length=0,
            lyric=Lyric(
                id_='123',
                track_id='456',
                common_track_id='789',
                content=['lyric1', 'lyric2']
            )
        )

    def test_publish_track(self, twitter, track):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        track_tweet = gorrion.publish_track(track)

        assert track_tweet == PublishedTweet(
            id_='fake-status-id',
            tweet=(
                'Now listening 🔊🎶:\n\n'
                'Track: 1. Peligro\n'
                'Album: Pa morirse de amor\n'
                'Artist: Ely Guerra\n\n'
                '#gorrion #NowPlaying #ElyGuerra\n\n'
                'http://spotify.com/track/1'
            ),
            entity=Album(
                id_='11',
                name='Pa morirse de amor',
                href='',
                public_url='http://spotify.com/album/11',
                release_date='2006-01-01',
                total_tracks=19,
                artists=[
                    Artist(
                        id_='12',
                        name='Ely Guerra',
                        href='',
                        public_url='http://spotify.com/artist/12',
                    )
                ],
                tracks=[
                    Track(
                        id_='1',
                        name='Peligro',
                        href='',
                        public_url='http://spotify.com/track/1',
                        disc_number=1,
                        track_number=1,
                        duration=1000,
                    )
                ],
            )
        )

    def test_publish_lyrics(self, twitter, song, lyric):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        published_track = PublishedTweet('1', 'track', None)
        song.lyric = lyric
        published_lyrics = gorrion.publish_lyrics(published_track, song)

        assert published_lyrics == [
            PublishedTweet(id_='fake-status-id', tweet='lyric1', entity=None),
            PublishedTweet(id_='fake-status-id', tweet='lyric2', entity=None),
        ]

    def test_publish_lyrics_when_lyric_not_found(self, twitter, song):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        published_track = PublishedTweet('1', 'track', None)
        published_lyrics = gorrion.publish_lyrics(published_track, song)

        assert published_lyrics == []

    def test_publish_album(self, twitter, track):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        album_tweet = gorrion.publish_album(track)

        assert album_tweet == PublishedTweet(
            id_='fake-status-id',
            tweet=(
                'Now listening 🔊🎶:\n\n'
                'Album: Pa morirse de amor\n'
                'Artist: Ely Guerra\n'
                'Tracks: 19\n'
                'Release: 2006\n\n'
                '#gorrion #NowPlaying #PaMorirseDeAmor #ElyGuerra\n\n'
                'http://spotify.com/album/11?si=g'
            ),
            entity=Album(
                id_='11',
                name='Pa morirse de amor',
                href='',
                public_url='http://spotify.com/album/11',
                release_date='2006-01-01',
                total_tracks=19,
                artists=[
                    Artist(
                        id_='12',
                        name='Ely Guerra',
                        href='',
                        public_url='http://spotify.com/artist/12',
                    )
                ],
                tracks=[
                    Track(
                        id_='1',
                        name='Peligro',
                        href='',
                        public_url='http://spotify.com/track/1',
                        disc_number=1,
                        track_number=1,
                        duration=1000,
                    )
                ],
            )
        )

    def test_full_song_status(self, twitter, track):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        status = gorrion.build_status(track, TweetSongConfig())
        assert status == ('Now listening 🔊🎶:\n\n'
                          'Track: 1. Peligro\n'
                          'Album: Pa morirse de amor\n'
                          'Artist: Ely Guerra\n\n'
                          '#gorrion #NowPlaying #ElyGuerra\n\n'
                          'http://spotify.com/track/1')

    def test_short_song_status(self, twitter, track):
        twitter.MAX_TWEET_LENGTH = 10
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        status = gorrion.build_status(track, TweetSongConfig())
        assert status == ('Now listening 🔊🎶:\n\n'
                          'Track: 1. Peligro\n'
                          'Album: Pa morirse de amor\n'
                          'Artist: Ely Guerra\n\n'
                          '#gorrion #NowPlaying\n\n'
                          'http://spotify.com/track/1')

    def test_full_album_status(self, twitter, track):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        status = gorrion.build_status(track, TweetAlbumConfig())
        assert status == ('Now listening 🔊🎶:\n\n'
                          'Album: Pa morirse de amor\n'
                          'Artist: Ely Guerra\n'
                          'Tracks: 19\n'
                          'Release: 2006\n\n'
                          '#gorrion #NowPlaying #PaMorirseDeAmor #ElyGuerra\n\n'
                          'http://spotify.com/album/11?si=g')

    def test_short_album_status(self, twitter, track):
        twitter.MAX_TWEET_LENGTH = 10
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        status = gorrion.build_status(track, TweetAlbumConfig())
        assert status == ('Now listening 🔊🎶:\n\n'
                          'Album: Pa morirse de amor\n'
                          'Artist: Ely Guerra\n'
                          'Tracks: 19\n'
                          'Release: 2006\n\n'
                          '#gorrion #NowPlaying #PaMorirseDeAmor\n\n'
                          'http://spotify.com/album/11?si=g')

    def test_is_valid_tweet_status_when_valid_status(self, twitter):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        assert gorrion.is_valid_tweet_status('1' * 280)

    def test_is_valid_tweet_status_when_invalid_status(self, twitter):
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())

        assert not gorrion.is_valid_tweet_status('1' * 281)

    def test_lyrics_to_tweets_short_lyrics(self, twitter):
        lyrics = ['lyric1', 'lyric2', 'lyric3']
        gorrion = Gorrion(MagicMock(), twitter, MagicMock())
        tweets = gorrion.lyrics_to_tweets(lyrics)

        assert tweets == ['lyric1', 'lyric2', 'lyric3']
