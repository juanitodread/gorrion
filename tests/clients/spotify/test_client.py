from unittest.mock import patch, MagicMock

import pytest

from src.clients.spotify.client import Spotify
from src.clients.spotify.errors import ServiceError, NotPlayingError
from src.clients.spotify.models import Track, Album, Artist


class TestSpotify:
    def test_constructor(self):
        spotify = Spotify('client_id', 'client_secret', 'refresh_token')
        
        assert spotify._client_id == 'client_id'
        assert spotify._client_secret == 'client_secret'
        assert spotify._refresh_token == 'refresh_token'

    @patch('src.clients.spotify.client.requests')
    def test_refresh_access_token(self, requests_mock):
        requests_mock.post.return_value = self._build_response_mock(
            json={'access_token': '92170cdc034b2ff819323ff670d3b7266c8bffcd'}
        )
        
        spotify = Spotify('client_id', 'client_secret', 'refresh_token')
        token = spotify.refresh_access_token()

        assert token == '92170cdc034b2ff819323ff670d3b7266c8bffcd'

    @patch('src.clients.spotify.client.requests')
    def test_refresh_token_when_error_response(self, requests_mock):
        requests_mock.post.return_value = self._build_response_mock(code=500, text='internal server error')

        spotify = Spotify('client_id', 'client_secret', 'refresh_token')

        with pytest.raises(ServiceError) as error:
            spotify.refresh_access_token()
        
        assert str(error.value) == 'Response API error: response="internal server error"'

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify.refresh_access_token')
    def test_get_current_track(self, refresh_access_token_mock, requests_mock):
        json_response = {
            'item': {
                'id': '1',
                'name': 'Peligro',
                'href': '',
                'track_number': 1,
                'external_urls': {
                    'spotify': 'https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1',
                },
                'album': {
                    'id': '11',
                    'name': 'Pa morirse de amor',
                    'href': '',
                    'release_date': '2006-01-01',
                },
                'artists': [
                    {
                        'id': '12',
                        'name': 'Ely Guerra',
                        'href': '',
                    }
                ]
            }
        }
        requests_mock.get.return_value = self._build_response_mock(code=200, json=json_response)

        spotify = Spotify('client_id', 'client_secret', 'refresh_token')
        track = spotify.get_current_track()

        assert track == Track(
            '1', 'Peligro', '', 1, 'https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1',
            Album('11', 'Pa morirse de amor', '', '2006-01-01'),
            [
                Artist('12', 'Ely Guerra', '')
            ]
        )

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify.refresh_access_token')
    def test_get_current_track_when_not_playing_error(self, refresh_access_token_mock, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(code=204, text='')

        spotify = Spotify('client_id', 'client_secret', 'refresh_token')

        with pytest.raises(NotPlayingError) as error:
            track = spotify.get_current_track()

        assert str(error.value) == 'Not playing any song at this moment'

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify.refresh_access_token')
    def test_get_current_track_when_error_response(self, refresh_access_token_mock, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(code=500, text='internal server error')

        spotify = Spotify('client_id', 'client_secret', 'refresh_token')

        with pytest.raises(ServiceError) as error:
            track = spotify.get_current_track()

        assert str(error.value) == 'Response API error: response="internal server error"'

    def test_get_basic_auth_token(self):
        spotify = Spotify('client_id', 'client_secret', 'refresh_token')

        basic_auth_token = spotify.get_basic_auth_token()

        assert basic_auth_token == 'Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ='

    def _build_response_mock(self, code: int=200, text: str='', json: dict=None):
        response_mock = MagicMock()
        response_mock.status_code = code
        response_mock.text = text
        response_mock.json.return_value = json if json else {}

        return response_mock
