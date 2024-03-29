from unittest.mock import patch, MagicMock

import pytest

from src.clients.spotify.client import (
    Spotify,
    SpotifyConfig,
    ServiceError, NotPlayingError,
    Track, Album, Artist,
)


@pytest.fixture()
def spotify() -> Spotify:
    config = SpotifyConfig('client_id', 'client_secret', 'refresh_token')
    return Spotify(config)


class TestSpotify:
    def test_constructor(self, spotify):
        assert spotify._client_id == 'client_id'
        assert spotify._client_secret == 'client_secret'
        assert spotify._refresh_token == 'refresh_token'

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify._refresh_access_token')
    def test_get_current_track(self,
                               refresh_access_token_mock,
                               requests_mock,
                               spotify):
        json_response = {
            'item': {
                'id': '1',
                'name': 'Peligro',
                'href': '',
                'track_number': 1,
                'external_urls': {
                    'spotify': 'https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1',
                },
                'disc_number': 1,
                'duration_ms': 1000,
                'album': {
                    'id': '11',
                    'name': 'Pa morirse de amor',
                    'href': '',
                    'external_urls': {
                        'spotify': 'https://open.spotify.com/album/0KSsZsTzIpqTRtbMaI67k1',
                    },
                    'release_date': '2006-01-01',
                    'total_tracks': 19,
                },
                'artists': [
                    {
                        'id': '12',
                        'name': 'Ely Guerra',
                        'href': '',
                        'external_urls': {
                            'spotify': 'https://open.spotify.com/artist/0KSsZsTzIpqTRtbMaI67k1',
                        },
                    }
                ]
            }
        }
        requests_mock.get.return_value = self._build_response_mock(
            code=200,
            json=json_response
        )
        album = spotify.get_current_track()

        assert album == Album(
            id_='11',
            name='Pa morirse de amor',
            href='',
            public_url='https://open.spotify.com/album/0KSsZsTzIpqTRtbMaI67k1',
            release_date='2006-01-01',
            total_tracks=19,
            artists=[
                Artist(
                    id_='12',
                    name='Ely Guerra',
                    href='',
                    public_url='https://open.spotify.com/artist/0KSsZsTzIpqTRtbMaI67k1',
                )
            ],
            tracks=[
                Track(
                    id_='1',
                    name='Peligro',
                    href='',
                    public_url='https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1',
                    disc_number=1,
                    track_number=1,
                    duration=1000,
                )
            ],
        )

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify._refresh_access_token')
    def test_get_current_track_when_not_playing_error(self,
                                                      refresh_access_token_mock,
                                                      requests_mock,
                                                      spotify):
        requests_mock.get.return_value = self._build_response_mock(
            code=204,
            text=''
        )

        with pytest.raises(NotPlayingError) as error:
            _ = spotify.get_current_track()

        assert str(error.value) == 'Not playing any song at this moment'

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify._refresh_access_token')
    def test_get_current_track_when_error_response(self,
                                                   refresh_access_token_mock,
                                                   requests_mock,
                                                   spotify):
        requests_mock.get.return_value = self._build_response_mock(
            code=500,
            json={'error': 'internal server error'}
        )

        with pytest.raises(ServiceError) as error:
            _ = spotify.get_current_track()

        assert str(error.value) == (
            "Response API error:\n\nReason: {'header': {}, "
            "'body': {'error': 'internal server error'}}"
        )

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify._get_current_playing')
    @patch('src.clients.spotify.client.Spotify._refresh_access_token')
    def test_get_current_album(self,
                               _refresh_access_token_mock,
                               _get_current_playing_mock,
                               requests_mock,
                               spotify):
        _get_current_playing_mock.return_value = {
            'item': {
                'album': {
                    'id': '11',
                }
            }
        }

        requests_mock.get.return_value = self._build_response_mock(
            json={
                'id': '11',
                'name': 'Pa morirse de amor',
                'href': '',
                'external_urls': {
                    'spotify': 'https://open.spotify.com/album/0KSsZsTzIpqTRtbMaI67k1'
                },
                'release_date': '2006-01-01',
                'total_tracks': 19,
                'artists': [{
                    'id': '12',
                    'name': 'Ely Guerra',
                    'href': '',
                    'external_urls': {
                        'spotify': 'https://open.spotify.com/artist/0KSsZsTzIpqTRtbMaI67k1'
                    }
                }],
                'tracks': {
                    'items': [{
                        'id': '1',
                        'name': 'Peligro',
                        'href': '',
                        'external_urls': {
                            'spotify': 'https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1'
                        },
                        'disc_number': 1,
                        'track_number': 1,
                        'duration_ms': 1000,
                    }, {
                        'id': '2',
                        'name': 'Take Five',
                        'href': '',
                        'external_urls': {
                            'spotify': 'https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1'
                        },
                        'disc_number': 1,
                        'track_number': 2,
                        'duration_ms': 1300,
                    }],
                }
            }
        )

        album = spotify.get_current_album()

        assert album == Album(
            id_='11',
            name='Pa morirse de amor',
            href='',
            public_url='https://open.spotify.com/album/0KSsZsTzIpqTRtbMaI67k1',
            release_date='2006-01-01',
            total_tracks=19,
            artists=[
                Artist(
                    id_='12',
                    name='Ely Guerra',
                    href='',
                    public_url='https://open.spotify.com/artist/0KSsZsTzIpqTRtbMaI67k1',
                )
            ],
            tracks=[
                Track(
                    id_='1',
                    name='Peligro',
                    href='',
                    public_url='https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1',
                    disc_number=1,
                    track_number=1,
                    duration=1000,
                ),
                Track(
                    id_='2',
                    name='Take Five',
                    href='',
                    public_url='https://open.spotify.com/track/0KSsZsTzIpqTRtbMaI67k1',
                    disc_number=1,
                    track_number=2,
                    duration=1300,
                ),
            ],
        )

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify._refresh_access_token')
    def test_get_current_album_when_not_playing_error(self,
                                                      _refresh_access_token_mock,
                                                      requests_mock,
                                                      spotify):
        requests_mock.get.return_value = self._build_response_mock(
            code=204,
            text=''
        )

        with pytest.raises(NotPlayingError) as error:
            _ = spotify.get_current_album()

        assert str(error.value) == 'Not playing any song at this moment'

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify._refresh_access_token')
    def test_get_current_album_when_error_response(self,
                                                   _refresh_access_token_mock,
                                                   requests_mock,
                                                   spotify):
        requests_mock.get.return_value = self._build_response_mock(
            code=500,
            json={'error': 'internal server error'}
        )

        with pytest.raises(ServiceError) as error:
            _ = spotify.get_current_album()

        assert str(error.value) == (
            "Response API error:\n\nReason: {'header': {}, "
            "'body': {'error': 'internal server error'}}"
        )

    @patch('src.clients.spotify.client.requests')
    @patch('src.clients.spotify.client.Spotify._refresh_access_token')
    def test_get_current_album_when_album_error_response(self,
                                                         _refresh_access_token_mock,
                                                         requests_mock,
                                                         spotify):
        requests_mock.get.side_effect = [
            self._build_response_mock(
                code=200,
                json={
                    'item': {
                        'album': {
                            'id': '11',
                        }
                    }
                }
            ), self._build_response_mock(
                code=500,
                json={'error': 'internal server error'}
            )
        ]

        with pytest.raises(ServiceError) as error:
            _ = spotify.get_current_album()

        assert requests_mock.get.call_count == 2
        assert str(error.value) == (
            "Response API error:\n\nReason: {'header': {}, "
            "'body': {'error': 'internal server error'}}"
        )

    @patch('src.clients.spotify.client.requests')
    def test_refresh_access_token(self, requests_mock, spotify):
        requests_mock.post.return_value = self._build_response_mock(
            json={'access_token': '92170cdc034b2ff819323ff670d3b7266c8bffcd'}
        )

        token = spotify._refresh_access_token()

        assert token == '92170cdc034b2ff819323ff670d3b7266c8bffcd'

    @patch('src.clients.spotify.client.requests')
    def test_refresh_token_when_error_response(self, requests_mock, spotify):
        requests_mock.post.return_value = self._build_response_mock(
            code=500,
            json={'error': 'internal server error'}
        )

        with pytest.raises(ServiceError) as error:
            _ = spotify._refresh_access_token()

        assert str(error.value) == (
            "Response API error:\n\nReason: {'header': {}, "
            "'body': {'error': 'internal server error'}}"
        )

    def test_get_basic_auth_token(self, spotify):
        basic_auth_token = spotify._get_basic_auth_token()

        assert basic_auth_token == 'Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ='

    def _build_response_mock(self,
                             code: int = 200,
                             text: str = '',
                             json: dict = None):
        response_mock = MagicMock()
        response_mock.status_code = code
        response_mock.text = text
        response_mock.json.return_value = json if json else {}

        return response_mock
