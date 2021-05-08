from unittest.mock import patch, MagicMock

import pytest

from src.clients.musixmatch.client import (
    Musixmatch,
    MusixmatchConfig,
    Song, Track, Lyric,
    SongNotFound, ServiceError,
)


@pytest.fixture()
def musixmatch() -> Musixmatch:
    config = MusixmatchConfig('api_key')
    return Musixmatch(config)


@pytest.fixture()
def song() -> Song:
    return Song(
        'Cumbiera Intelectual',
        'Kevin Johansen',
        'En Vivo',
        [],
        1,
        None,
    )


class TestMusixmatch:
    def test_constructor(self, musixmatch):
        assert musixmatch._api_key == 'api_key'

    @patch('src.clients.musixmatch.client.requests')
    def test_search_song(self, requests_mock, musixmatch, song):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'track_list': [
                    {
                        'track': {
                            'track_id': '123',
                            'commontrack_id': '456',
                            'track_name': 'Cumbiera Intelectual',
                            'instrumental': 0,
                            'explicit': 0,
                            'album_name': 'En Vivo',
                            'artist_name': 'Kevin Johansen',
                        }
                    }
                ]
            }
        )

        song_found = musixmatch.search_song(song)

        assert song_found == Song(
            name='Cumbiera Intelectual',
            artist='Kevin Johansen',
            album='En Vivo',
            tracks=[
                Track(
                    id_='123',
                    common_id='456',
                    name='Cumbiera Intelectual',
                    instrumental=0,
                    explicit=0,
                    artist='Kevin Johansen',
                    album='En Vivo'
                )
            ],
            tracks_length=1,
            lyric=None
        )

    @patch('src.clients.musixmatch.client.requests')
    def test_search_song_when_song_not_found(self, requests_mock, musixmatch):
        requests_mock.get.return_value = self._build_response_mock(
            code=404,
            json={}
        )

        with pytest.raises(SongNotFound) as error:
            track_id, common_track_id = musixmatch.search_song(
                Song('Cumbiera No Intelectual', 'Kevin Johansen', 'En Vivo'))

        assert str(error.value) == (
            "Song not found: song=Song(name='Cumbiera No Intelectual', "
            "artist='Kevin Johansen', album='En Vivo', tracks=None, "
            "tracks_length=0, lyric=None)"
        )

    @patch('src.clients.musixmatch.client.requests')
    def test_search_song_when_service_error(self,
                                            requests_mock,
                                            musixmatch,
                                            song):
        requests_mock.get.return_value = self._build_response_mock(
            code=500,
            json={}
        )

        with pytest.raises(ServiceError) as error:
            track_id, common_track_id = musixmatch.search_song(song)

        assert str(error.value) == 'Response API error: response="500"'

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric(self, requests_mock, musixmatch, song):
        requests_mock.get.return_value = self._build_response_mock(
            json={
                'lyrics': {
                    'lyrics_body': 'Gotita de mezcal',
                }
            }
        )

        song.lyric = Lyric('987', '123', '456', ['Gotita de mezcal'])
        song_found = musixmatch.fetch_lyric(song)

        assert song_found.lyric == Lyric(
            '987',
            '123',
            '456',
            ['Gotita de mezcal']
        )

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric_when_lyric_not_found(self,
                                              requests_mock,
                                              musixmatch,
                                              song):
        requests_mock.get.return_value = self._build_response_mock(json=[])

        song_found = musixmatch.fetch_lyric(song)

        assert song_found.lyric is None

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric_when_service_error(self,
                                            requests_mock,
                                            musixmatch,
                                            song):
        requests_mock.get.return_value = self._build_response_mock(json=[])

        song_found = musixmatch.fetch_lyric(song)

        assert song_found.lyric is None

    @patch('src.clients.musixmatch.client.requests')
    def test_fetch_lyric_when_lyric_not_provided_yet(self,
                                                     requests_mock,
                                                     musixmatch,
                                                     song):
        requests_mock.get.return_value = self._build_response_mock(json=[])

        song_found = musixmatch.fetch_lyric(song)

        assert song_found.lyric is None

    def _build_response_mock(self,
                             code: int = 200,
                             text: str = '',
                             json: dict = None):
        response_mock = MagicMock()
        response_mock.status_code = code
        response_mock.text = text
        response_mock.json.return_value = {
            'message': {
                'header': {
                    'status_code': code,
                },
                'body': json,
            }
        } if json is not None else {}

        return response_mock
