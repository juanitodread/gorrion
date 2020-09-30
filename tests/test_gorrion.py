from unittest.mock import patch, MagicMock

from src.gorrion import Gorrion
from src.config import Config

class TestGorrion:
    @patch('src.gorrion.Spotify')
    def test_run(self, spotify_mock):
        get_current_track_mock = MagicMock()
        spotify_mock.return_value.get_current_track = get_current_track_mock

        gorrion = Gorrion()
        gorrion.run()

        spotify_mock.assert_called_once_with(
            Config.SPOTIFY_CLIENT_ID, 
            Config.SPOTIFY_CLIENT_SECRET, 
            Config.SPOTIFY_REFRESH_TOKEN,
        )
        get_current_track_mock.assert_called_once_with()
