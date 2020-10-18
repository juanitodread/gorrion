from unittest.mock import patch, MagicMock

from src.gorrion import Gorrion
from src.config import Config
from src.clients.spotify.models import Track, Album, Artist

class TestGorrion:
    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Twitter')
    @patch('src.gorrion.Musixmatch')
    def test_constructor(self, musixmatch_mock, twitter_mock, spotify_mock):
        gorrion = Gorrion()

        spotify_mock.assert_called_once_with(
            Config.SPOTIFY_CLIENT_ID, 
            Config.SPOTIFY_CLIENT_SECRET, 
            Config.SPOTIFY_REFRESH_TOKEN,
        )
        twitter_mock.assert_called_once_with(
            Config.TWITTER_API_CONSUMER_KEY,
            Config.TWITTER_API_CONSUMER_SECRET,
            Config.TWITTER_API_ACCESS_TOKEN,
            Config.TWITTER_API_ACCESS_TOKEN_SECRET,
        )
        musixmatch_mock.assert_called_once_with(
            Config.MUSIXMATCH_API_KEY,
        )

        assert gorrion._spotify != None
        assert gorrion._twitter != None
        assert gorrion._musixmatch != None

    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Musixmatch')
    @patch('builtins.print')
    def test_playing_full_status(self, print_mock, musixmatch_mock, spotify_mock):
        get_current_track_mock = MagicMock(return_value=Track(
            '1', 'Peligro', '', 1, '',
            Album('11', 'Pa morirse de amor', '', '2006-01-01'),
            [
                Artist('12', 'Ely Guerra', '')
            ]
        ))

        spotify_mock.return_value.get_current_track = get_current_track_mock
        musixmatch_mock.return_value.search_song.return_value = ('1', '2')

        gorrion = Gorrion()
        gorrion.playing(disable_twitter=True)

        get_current_track_mock.assert_called_once_with()
        print_mock.assert_any_call('Now listening 🔊🎶: \n\n'
                                   'Track: 1. Peligro\nAlbum: Pa morirse de amor\n'
                                   'Artist: Ely Guerra\n\n#gorrion #NowPlaying #ElyGuerra\n\n')

    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Musixmatch')
    @patch('builtins.print')
    def test_playing_short_status(self, print_mock, musixmatch_mock, spotify_mock):
        get_current_track_mock = MagicMock(return_value=Track(
            '1',
            'Barcelona, Ciutat Refugi', 
            'https://api.spotify.com/v1/tracks/72NWtDFShJ2gVVVL41UlHZ', 
            3,
            'https://open.spotify.com/track/72NWtDFShJ2gVVVL41UlHZ',
            Album('11', 'Black is beltza ASM Sessions', '', '2006-01-01'),
            [
                Artist('12', 'Fermin Muguruza', ''),
                Artist('13', 'Chalart58', ''),
                Artist('14', 'Chrishira Perrier', ''),
                Artist('15', 'Ashlin Parker', ''),
                Artist('16', 'Vic Navarrete', ''),
            ]
        ))

        spotify_mock.return_value.get_current_track = get_current_track_mock
        musixmatch_mock.return_value.search_song.return_value = ('1', '2')

        gorrion = Gorrion()
        gorrion.playing(disable_twitter=True)

        get_current_track_mock.assert_called_once_with()

        print_mock.assert_any_call('(Using short status)')
        print_mock.assert_any_call('Now listening 🔊🎶: \n\n'
                                   'Track: 3. Barcelona, Ciutat Refugi\n'
                                   'Album: Black is beltza ASM Sessions\n'
                                   'Artist: Fermin Muguruza, Chalart58, Chrishira Perrier, Ashlin Parker, Vic Navarrete\n\n'
                                   '#gorrion #NowPlaying\n\nhttps://open.spotify.com/track/72NWtDFShJ2gVVVL41UlHZ')

    @patch('src.gorrion.Musixmatch')
    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Twitter')
    def test_playing_disable_twitter(self, twitter_mock, spotify_mock, musixmatch_mock):
        get_current_track_mock = MagicMock()
        twitter_post_mock = MagicMock()

        spotify_mock.return_value.get_current_track = get_current_track_mock
        twitter_mock.return_value.post = twitter_post_mock
        twitter_mock.return_value.max_tweet_length = 280
        musixmatch_mock.return_value.search_song.return_value = ('1', '2')

        gorrion = Gorrion()
        gorrion.playing(disable_twitter=True)

        get_current_track_mock.assert_called_once_with()
        twitter_post_mock.assert_not_called()

    @patch('src.gorrion.Musixmatch')
    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Twitter')
    def test_playing_enable_twitter(self, twitter_mock, spotify_mock, musixmatch_mock):
        get_current_track_mock = MagicMock(return_value=Track(
            '1', 'Peligro', '', 1, '',
            Album('11', 'Pa morirse de amor', '', '2006-01-01'),
            [
                Artist('12', 'Ely Guerra', '')
            ]
        ))
        twitter_post_mock = MagicMock()

        spotify_mock.return_value.get_current_track = get_current_track_mock
        twitter_mock.return_value.post = twitter_post_mock
        twitter_mock.return_value.max_tweet_length = 280
        musixmatch_mock.return_value.search_song.return_value = ('1', '2')

        gorrion = Gorrion()
        gorrion.playing()

        get_current_track_mock.assert_called_once_with()
        twitter_post_mock.assert_called_once_with('Now listening 🔊🎶: \n\n'
                                                  'Track: 1. Peligro\nAlbum: Pa morirse de amor\n'
                                                  'Artist: Ely Guerra\n\n#gorrion #NowPlaying #ElyGuerra\n\n')
