import pytest

from atproto_client.utils import TextBuilder

from src.clients.spotify import Track, Album, Artist
from src.templates import BlueskyTemplate, TweetConfig, TweetSongConfig
from src.templates.bluesky import BodyTemplate, FooterTemplate


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


@pytest.fixture()
def text_builder_fixture():
    return TextBuilder()


class TestBlueskyTemplate:
    def test_constructor(self, album_fixture, config_fixture):
        template = BlueskyTemplate(album_fixture, config_fixture)

        assert template._album == album_fixture
        assert template._config == config_fixture

    def test_to_tweet_with_header_only(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = True
        song_config_fixture.with_body = False
        song_config_fixture.with_footer = False
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        text = template.to_tweet().build_text()

        assert text == 'Now listening 🔊🎶:\n\n'

    def test_to_tweet_with_body_only(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = False
        song_config_fixture.with_body = True
        song_config_fixture.with_footer = False
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        text = template.to_tweet().build_text()

        assert text == ('Track: 1. Peligro\n'
                        'Album: Pa morirse de amor\n'
                        'Artist: Ely Guerra\n\n')

    def test_to_tweet_with_footer_only(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = False
        song_config_fixture.with_body = False
        song_config_fixture.with_footer = True
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        text = template.to_tweet().build_text()

        assert text == ('#gorrion #NowPlaying #ElyGuerra \n\n'
                        'http://spotify.com/track/1')

    def test_to_tweet_default_config(self, album_fixture, config_fixture):
        template = BlueskyTemplate(album_fixture, config_fixture)
        text = template.to_tweet().build_text()

        assert text == ''

    def test_header_with_header_true(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = True
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        template.header()
        text = template.to_text()

        assert text == 'Now listening 🔊🎶:\n\n'

    def test_header_with_header_false(self, album_fixture, song_config_fixture):
        song_config_fixture.with_header = False
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        template.header()
        text = template.to_text()

        assert text == ''

    def test_body_with_body_true(self, album_fixture, song_config_fixture):
        song_config_fixture.with_body = True
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        template.body()
        text = template.to_text()

        assert text == ('Track: 1. Peligro\n'
                        'Album: Pa morirse de amor\n'
                        'Artist: Ely Guerra\n\n')

    def test_body_with_body_false(self, album_fixture, song_config_fixture):
        song_config_fixture.with_body = False
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        template.body()
        text = template.to_text()

        assert text == ''

    def test_footer_with_footer_true(self, album_fixture, song_config_fixture):
        song_config_fixture.with_footer = True
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        template.footer()
        text = template.to_text()

        assert text == ('#gorrion #NowPlaying #ElyGuerra \n\n'
                        'http://spotify.com/track/1')

    def test_footer_with_footer_false(self, album_fixture, song_config_fixture):
        song_config_fixture.with_footer = False
        template = BlueskyTemplate(album_fixture, song_config_fixture)
        template.footer()
        text = template.to_text()

        assert text == ''


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
    def test_constructor(self, album_fixture, config_fixture, text_builder_fixture):
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)

        assert footer_template._album == album_fixture
        assert footer_template._config == config_fixture.footer_config

    def test_to_footer_with_hashtags_only(self, album_fixture, config_fixture, text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = True
        config_fixture.footer_config.with_album_hashtag = True
        config_fixture.footer_config.with_artists_hashtag = True
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        text = footer_template.to_footer().build_text()

        assert text == ('#gorrion #NowPlaying '
                        '#PaMorirseDeAmor '
                        '#ElyGuerra \n\n')

    def test_to_footer_with_gorrion_hashtags_only(self, album_fixture, config_fixture, text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = True
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        text = footer_template.to_footer().build_text()

        assert text == '#gorrion #NowPlaying \n\n'

    def test_to_footer_with_album_hashtag_only(self, album_fixture, config_fixture, text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = True
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        text = footer_template.to_footer().build_text()

        assert text == '#PaMorirseDeAmor \n\n'

    def test_to_footer_with_artists_hashtag_only(self, album_fixture, config_fixture, text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = True
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        text = footer_template.to_footer().build_text()

        assert text == '#ElyGuerra \n\n'

    def test_to_footer_with_song_media_link_only(self, album_fixture, config_fixture, text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = True
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        text = footer_template.to_footer().build_text()

        assert text == '\n\nhttp://spotify.com/track/1'

    def test_to_footer_with_album_media_link_only(self, album_fixture, config_fixture, text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        text = footer_template.to_footer().build_text()

        assert text == '\n\nhttp://spotify.com/album/11?si=g'

    def test_to_footer_default_config(self, album_fixture, config_fixture, text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        config_fixture.footer_config.with_album_hashtag = False
        config_fixture.footer_config.with_artists_hashtag = False
        config_fixture.footer_config.with_song_media_link = False
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        text = footer_template.to_footer().build_text()

        assert text == '\n\n'

    def test_gorrion_hashtags_with_gorrion_hashtags_true(self,
                                                         album_fixture,
                                                         config_fixture,
                                                         text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.gorrion_hashtags()
        text = footer_template._text_builder.build_text()

        assert text == '#gorrion #NowPlaying '

    def test_gorrion_hashtags_with_gorrion_hashtags_false(self,
                                                          album_fixture,
                                                          config_fixture,
                                                          text_builder_fixture):
        config_fixture.footer_config.with_gorrion_hashtags = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.gorrion_hashtags()
        text = footer_template._text_builder.build_text()

        assert text == ''

    def test_album_hashtags_with_album_hashtag_true(self,
                                                    album_fixture,
                                                    config_fixture,
                                                    text_builder_fixture):
        config_fixture.footer_config.with_album_hashtag = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.album_hashtags()
        text = footer_template._text_builder.build_text()

        assert text == '#PaMorirseDeAmor '

    def test_album_hashtags_with_album_hashtag_false(self,
                                                     album_fixture,
                                                     config_fixture,
                                                     text_builder_fixture):
        config_fixture.footer_config.with_album_hashtag = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.album_hashtags()
        text = footer_template._text_builder.build_text()

        assert text == ''

    def test_artists_hashtags_with_artists_hashtag_true(self,
                                                        album_fixture,
                                                        config_fixture,
                                                        text_builder_fixture):
        config_fixture.footer_config.with_artists_hashtag = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.artists_hashtags()
        text = footer_template._text_builder.build_text()

        assert text == '#ElyGuerra '

    def test_artists_hashtags_with_artists_hashtag_false(self,
                                                         album_fixture,
                                                         config_fixture,
                                                         text_builder_fixture):
        config_fixture.footer_config.with_artists_hashtag = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.artists_hashtags()
        text = footer_template._text_builder.build_text()

        assert text == ''

    def test_song_media_link_with_song_media_link_true(self,
                                                       album_fixture,
                                                       config_fixture,
                                                       text_builder_fixture):
        config_fixture.footer_config.with_song_media_link = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.song_media_link()
        text = footer_template._text_builder.build_text()

        assert text == 'http://spotify.com/track/1'

    def test_song_media_link_with_song_media_link_false(self,
                                                        album_fixture,
                                                        config_fixture,
                                                        text_builder_fixture):
        config_fixture.footer_config.with_song_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.song_media_link()
        text = footer_template._text_builder.build_text()

        assert text == ''

    def test_album_media_link_with_album_media_link_true(self,
                                                         album_fixture,
                                                         config_fixture,
                                                         text_builder_fixture):
        config_fixture.footer_config.with_album_media_link = True
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.album_media_link()
        text = footer_template._text_builder.build_text()

        assert text == 'http://spotify.com/album/11?si=g'

    def test_album_media_link_with_album_media_link_false(self,
                                                          album_fixture,
                                                          config_fixture,
                                                          text_builder_fixture):
        config_fixture.footer_config.with_album_media_link = False
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)
        footer_template.album_media_link()
        text = footer_template._text_builder.build_text()

        assert text == ''

    def test_build_hashtag(self, album_fixture, config_fixture, text_builder_fixture):
        footer_template = FooterTemplate(album_fixture, config_fixture.footer_config, text_builder_fixture)

        assert footer_template._build_hashtag('') == ''
        assert footer_template._build_hashtag('alpha-only') == 'Alphaonly'
        assert footer_template._build_hashtag('digit-only') == 'Digitonly'
        assert footer_template._build_hashtag('no more') == 'NoMore'
        assert footer_template._build_hashtag('  alone   ') == 'Alone'
        assert (footer_template
                ._build_hashtag('thIS iS a AM vAlID') == 'ThisIsAAMValid')
