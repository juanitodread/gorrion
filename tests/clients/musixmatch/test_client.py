from unittest.mock import patch, MagicMock

import pytest

from src.clients.musixmatch.client import Musixmatch
from src.clients.musixmatch.models import Song, Track, Lyric
from src.clients.musixmatch.errors import (
    SongNotFound,
    ServiceError,
    LyricNotFound,
    LyricNotProvidedYet
)


class TestMusixmatch:
    def test_constructor(self):
        musixmatch = Musixmatch('api_key')

        assert musixmatch._api_key == 'api_key'

    @patch('src.clients.musixmatch.client.requests')
    def test_search_song(self, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'message': {
                    'header': {
                        'status_code': 200,
                    },
                    'body': {
                        'track_list': [
                            {
                                'track': {
                                    'track_id': '123',
                                    'commontrack_id': '456',
                                    'track_name': 'Cumbiera Intelectual',
                                    'instrumental': 0,
                                    'explicit': 0,
                                    'album_name': 'Mi querido Brasil',
                                    'artist_name': 'Kevin Johansen',
                                }
                            }
                        ]
                    }
                }
            }
        )
        
        musixmatch = Musixmatch('api_key')
        song = musixmatch.search_song('Cumbiera Intelectual', 'Kevin Johansen', 'Mi querido Brasil')

        assert song == Song(
            name='Cumbiera Intelectual',
            artist='Kevin Johansen',
            album='Mi querido Brasil',
            tracks=[
                Track(
                    id_='123',
                    common_id='456',
                    name='Cumbiera Intelectual',
                    instrumental=0,
                    explicit=0,
                    artist='Kevin Johansen',
                    album='Mi querido Brasil'
                )
            ],
            tracks_length=1,
            lyric=None
        )

    @patch('src.clients.musixmatch.client.requests')
    def test_search_song_when_song_not_found(self, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'message': {
                    'header': {
                        'status_code': 404,
                    },
                    'body': {
                    }
                }
            }
        )
        
        musixmatch = Musixmatch('api_key')

        with pytest.raises(SongNotFound) as error:
            track_id, common_track_id = musixmatch.search_song('Cumbiera No Intelectual', 'Kevin Johansen', 'En Vivo')

        assert str(error.value) == ("Song not found: song=Song(name='Cumbiera No Intelectual', artist='Kevin "
                                    "Johansen', album='En Vivo', tracks=None, tracks_length=0, lyric=None)")

    @patch('src.clients.musixmatch.client.requests')
    def test_search_song_when_service_error(self, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'message': {
                    'header': {
                        'status_code': 500,
                    },
                    'body': {
                    }
                }
            }
        )
        
        musixmatch = Musixmatch('api_key')

        with pytest.raises(ServiceError) as error:
            track_id, common_track_id = musixmatch.search_song('Cumbiera Intelectual', 'Kevin Johansen', 'En Vivo')

        assert str(error.value) == 'Response API error: response="500"'

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric(self, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'message': {
                    'header': {
                        'status_code': 200,
                    },
                    'body': {
                        'lyrics': {
                            'lyrics_body': 'Gotita de mezcal',
                        }
                    }
                }
            }
        )
        
        musixmatch = Musixmatch('api_key')
        song = musixmatch.fetch_lyric(Song(
            'Cumbiera Intelectual',
            'Kevin Johansen',
            'En Vivo', 
            [
                Track('123', '456', 'Gotita de mezcal', 0, 0, '', '')
            ], 
            1, 
            Lyric('987', '123', '456', ['Gotita de mezcal']))
        )

        assert song.lyric == Lyric('987', '123', '456', ['Gotita de mezcal'])

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric_when_lyric_not_found(self, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'message': {
                    'header': {
                        'status_code': 404,
                    },
                    'body': []
                }
            }
        )
        
        musixmatch = Musixmatch('api_key')
        song = musixmatch.fetch_lyric(Song(
            'Cumbiera Intelectual',
            'Kevin Johansen',
            'En Vivo', 
            [], 
            1, 
            None)
        )

        assert song.lyric == None

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric_when_service_error(self, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'message': {
                    'header': {
                        'status_code': 500,
                    },
                    'body': []
                }
            }
        )
        
        musixmatch = Musixmatch('api_key')

        song = musixmatch.fetch_lyric(Song(
            'Cumbiera Intelectual',
            'Kevin Johansen',
            'En Vivo', 
            [], 
            1, 
            None)
        )

        assert song.lyric == None

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric_when_lyric_not_provided_yet(self, requests_mock):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'message': {
                    'header': {
                        'status_code': 200,
                    },
                    'body': []
                }
            }
        )
        
        musixmatch = Musixmatch('api_key')

        song = musixmatch.fetch_lyric(Song(
            'Cumbiera Intelectual',
            'Kevin Johansen',
            'En Vivo', 
            [], 
            1, 
            None)
        )

        assert song.lyric == None

    def _build_response_mock(self, code: int=200, text: str='', json: dict=None):
        response_mock = MagicMock()
        response_mock.status_code = code
        response_mock.text = text
        response_mock.json.return_value = json if json else {}

        return response_mock
