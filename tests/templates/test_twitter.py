import pytest

from src.clients.spotify import Track, Album, Artist
from src.templates import TweetTemplate, TweetConfig, TweetSongConfig
from src.templates.twitter import BodyTemplate, FooterTemplate


@pytest.fixture()
def album_fixture():
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
def config_fixture():
    return TweetConfig()


@pytest.fixture()
def song_config_fixture():
    return TweetSongConfig()


class TestTweetTemplate:
    def test_constructor(self, album_fixture, config_fixture):
        template = TweetTemplate(album_fixture, config_fixture)

        assert template._album == album_fixture
        assert template._config == config_fixture

    def test_to_tweet_with_header_only(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = True
        song_config_fixture.with_body = False
        song_config_fixture.with_footer = False
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.to_tweet() == 'Now listening 🔊🎶:\n\n'

    def test_to_tweet_with_body_only(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = False
        song_config_fixture.with_body = True
        song_config_fixture.with_footer = False
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.to_tweet() == ('Track: 1. Peligro\n'
                                       'Album: Pa morirse de amor\n'
                                       'Artist: Ely Guerra\n\n')

    def test_to_tweet_with_footer_only(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = False
        song_config_fixture.with_body = False
        song_config_fixture.with_footer = True
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.to_tweet() == ('#gorrion #NowPlaying\n\n'
                                       'http://spotify.com/track/1')

    def test_to_tweet_default_config(self, album_fixture, config_fixture):
        template = TweetTemplate(album_fixture, config_fixture)

        assert template.to_tweet() == ''

    def test_header_with_header_true(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = True
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.header() == 'Now listening 🔊🎶:\n\n'

    def test_header_with_header_false(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = False
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.header() == ''

    def test_body_with_body_true(self, album_fixture, song_config_fixture):
        song_config_fixture.with_body = True
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.body() == ('Track: 1. Peligro\n'
                                   'Album: Pa morirse de amor\n'
                                   'Artist: Ely Guerra\n\n')

    def test_body_with_body_false(self, album_fixture, song_config_fixture):
        song_config_fixture.with_body = False
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.body() == ''

    def test_footer_with_footer_true(self, album_fixture, song_config_fixture):
        song_config_fixture.with_footer = True
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.footer() == ('#gorrion #NowPlaying\n\n'
                                     'http://spotify.com/track/1')

    def test_footer_with_footer_false(self, album_fixture, song_config_fixture):
        song_config_fixture.with_footer = False
        template = TweetTemplate(album_fixture, song_config_fixture)

        assert template.footer() == ''


class TestBodyTemplate:
    def test_constructor(self, album_fixture, song_config_fixture):
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template._album == album_fixture
        assert body_template._config == song_config_fixture.body_config

    def test_to_body_with_track_only(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_track = True
        song_config_fixture.body_config.with_album = False
        song_config_fixture.body_config.with_artists = False
        song_config_fixture.body_config.with_tracks = False
        song_config_fixture.body_config.with_release_date = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.to_body() == 'Track: 1. Peligro\n'

    def test_to_body_with_album_only(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_track = False
        song_config_fixture.body_config.with_album = True
        song_config_fixture.body_config.with_artists = False
        song_config_fixture.body_config.with_tracks = False
        song_config_fixture.body_config.with_release_date = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.to_body() == 'Album: Pa morirse de amor\n'

    def test_to_body_with_artists_only(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_track = False
        song_config_fixture.body_config.with_album = False
        song_config_fixture.body_config.with_artists = True
        song_config_fixture.body_config.with_tracks = False
        song_config_fixture.body_config.with_release_date = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.to_body() == 'Artist: Ely Guerra\n'

    def test_to_body_with_tracks_only(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_track = False
        song_config_fixture.body_config.with_album = False
        song_config_fixture.body_config.with_artists = False
        song_config_fixture.body_config.with_tracks = True
        song_config_fixture.body_config.with_release_date = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.to_body() == 'Tracks: 19\n'

    def test_to_body_with_release_date_only(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_track = False
        song_config_fixture.body_config.with_album = False
        song_config_fixture.body_config.with_artists = False
        song_config_fixture.body_config.with_tracks = False
        song_config_fixture.body_config.with_release_date = True
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.to_body() == 'Release: 2006\n'

    def test_body_with_track_true(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_track = True
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.track() == 'Track: 1. Peligro\n'

    def test_body_with_track_false(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_track = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.track() == ''

    def test_body_with_album_true(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_album = True
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.album() == 'Album: Pa morirse de amor\n'

    def test_body_with_album_false(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_album = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.album() == ''

    def test_body_with_artists_true(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_artists = True
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.artists() == 'Artist: Ely Guerra\n'

    def test_body_with_artists_false(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_artists = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.artists() == ''

    def test_body_with_tracks_true(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_tracks = True
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.tracks() == 'Tracks: 19\n'

    def test_body_with_tracks_false(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_tracks = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.tracks() == ''

    def test_body_with_release_date_true(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_release_date = True
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.release_date() == 'Release: 2006\n'

    def test_body_with_release_date_false(self, album_fixture, song_config_fixture):
        song_config_fixture.body_config.with_release_date = False
        body_template = BodyTemplate(album_fixture, song_config_fixture.body_config)

        assert body_template.release_date() == ''

    def test_to_body_default_config(self, album_fixture, config_fixture):
        body_template = BodyTemplate(album_fixture, config_fixture.body_config)

        assert body_template.to_body() == ''


class TestFooterTemplate:
    def test_constructor(self, album_fixture, config_fixture):
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template._album == album_fixture
        assert footer_template._config == config_fixture.footer_config

    def test_to_footer_with_hashtags_only(self, album_fixture, config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = True
        config_fixture.footer_config.with_album_hashtag = True
        config_fixture.footer_config.with_artists_hashtag = True
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.to_footer() == ('#gorrion #NowPlaying '
                                               '#PaMorirseDeAmor '
                                               '#ElyGuerra\n\n')

    def test_to_footer_with_gorrion_hashtags_only(self, album_fixture, config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = True
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.to_footer() == '#gorrion #NowPlaying\n\n'

    def test_to_footer_with_album_hashtag_only(self, album_fixture, config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = True
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.to_footer() == '#PaMorirseDeAmor\n\n'

    def test_to_footer_with_artists_hashtag_only(self, album_fixture, config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = True
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.to_footer() == '#ElyGuerra\n\n'

    def test_to_footer_with_song_media_link_only(self, album_fixture, config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = True
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.to_footer() == 'http://spotify.com/track/1'

    def test_to_footer_with_album_media_link_only(self, album_fixture, config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.to_footer() == 'http://spotify.com/album/11?si=g'

    def test_to_footer_default_config(self, album_fixture, config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.to_footer() == ''

    def test_gorrion_hashtags_with_gorrion_hashtags_true(self,
                                                         album_fixture,
                                                         config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.gorrion_hashtags() == '#gorrion #NowPlaying '

    def test_gorrion_hashtags_with_gorrion_hashtags_false(self,
                                                          album_fixture,
                                                          config_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.gorrion_hashtags() == ''

    def test_album_hashtags_with_album_hashtag_true(self,
                                                    album_fixture,
                                                    config_fixture):
        config_fixture.footer_config.with_album_hashtag = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.album_hashtags() == '#PaMorirseDeAmor '

    def test_album_hashtags_with_album_hashtag_false(self,
                                                     album_fixture,
                                                     config_fixture):
        config_fixture.footer_config.with_album_hashtag = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.album_hashtags() == ''

    def test_artists_hashtags_with_artists_hashtag_true(self,
                                                        album_fixture,
                                                        config_fixture):
        config_fixture.footer_config.with_artists_hashtag = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.artists_hashtags() == '#ElyGuerra'

    def test_artists_hashtags_with_artists_hashtag_false(self,
                                                         album_fixture,
                                                         config_fixture):
        config_fixture.footer_config.with_artists_hashtag = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.artists_hashtags() == ''

    def test_song_media_link_with_song_media_link_true(self,
                                                       album_fixture,
                                                       config_fixture):
        config_fixture.footer_config.with_song_media_link = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.song_media_link() == 'http://spotify.com/track/1'

    def test_song_media_link_with_song_media_link_false(self,
                                                        album_fixture,
                                                        config_fixture):
        config_fixture.footer_config.with_song_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.song_media_link() == ''

    def test_album_media_link_with_album_media_link_true(self,
                                                         album_fixture,
                                                         config_fixture):
        config_fixture.footer_config.with_album_media_link = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert (footer_template
                .album_media_link() == 'http://spotify.com/album/11?si=g')

    def test_album_media_link_with_album_media_link_false(self,
                                                          album_fixture,
                                                          config_fixture):
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template.album_media_link() == ''

    def test_build_hashtag(self, album_fixture, config_fixture):
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config)

        assert footer_template._build_hashtag('') == ''
        assert footer_template._build_hashtag('alpha-only') == '#Alphaonly'
        assert footer_template._build_hashtag('digit-only') == '#Digitonly'
        assert footer_template._build_hashtag('no more') == '#NoMore'
        assert footer_template._build_hashtag('  alone   ') == '#Alone'
        assert (footer_template
                ._build_hashtag('thIS iS a AM vAlID') == '#ThisIsAAMValid')
