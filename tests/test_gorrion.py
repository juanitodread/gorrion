from unittest.mock import patch, MagicMock

from src.gorrion import Gorrion
from src.config import Config
from src.clients.spotify.models import Track, Album, Artist

class TestGorrion:
    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Twitter')
    def test_constructor(self, twitter_mock, spotify_mock):
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

        assert gorrion._spotify != None
        assert gorrion._twitter != None

    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Twitter')
    def test_playing_disable_twitter(self, twitter_mock, spotify_mock):
        get_current_track_mock = MagicMock()
        twitter_post_mock = MagicMock()

        spotify_mock.return_value.get_current_track = get_current_track_mock
        twitter_mock.return_value.post = twitter_post_mock

        gorrion = Gorrion()
        gorrion.playing(disable_twitter=True)

        get_current_track_mock.assert_called_once_with()
        twitter_post_mock.assert_not_called()

    @patch('src.gorrion.Spotify')
    @patch('src.gorrion.Twitter')
    def test_playing_enable_twitter(self, twitter_mock, spotify_mock):
        get_current_track_mock = MagicMock(return_value=Track(
            '1', 'Peligro', '', 1,
            Album('11', 'Pa morirse de amor', '', '2006-01-01'),
            [
                Artist('12', 'Ely Guerra', '')
            ]
        ))
        twitter_post_mock = MagicMock()

        spotify_mock.return_value.get_current_track = get_current_track_mock
        twitter_mock.return_value.post = twitter_post_mock

        gorrion = Gorrion()
        gorrion.playing()

        get_current_track_mock.assert_called_once_with()
        twitter_post_mock.assert_called_once_with('Now listening 🎶🔊: \n\n'
                                                  'Track: 1. Peligro\nAlbum: Pa morirse de amor\n'
                                                  'Artist: Ely Guerra\n\n#gorrion #NowPlaying\n\n')
