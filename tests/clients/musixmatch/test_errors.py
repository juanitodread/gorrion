from src.clients.musixmatch.errors import (
    MusixmatchApiError,
    ServiceError,
    SongNotFound,
    LyricNotFound,
    LyricNotProvidedYet,
)


class TestErrors:
    def test_musixmatch_api_error(self):
        error = MusixmatchApiError('error')

        assert str(error) == 'error'

    def test_service_error(self):
        error = ServiceError('service-error')

        assert str(error) == 'Response API error: response="service-error"'

    def test_song_not_found_error(self):
        error = SongNotFound('Coqueta')

        assert str(error) == 'Song not found: song=Coqueta'

    def test_lyric_not_found_error(self):
        error = LyricNotFound('123', '456')

        assert str(error) == ('Lyric not found. You may try another index: '
                              'track_id=123, common_track_id=456')

    def test_lyric_not_provided_yet(self):
        error = LyricNotProvidedYet('123', '456')

        assert str(error) == (
            'Lyric not provided for this song or song is instrumental. '
            'You may try another index: track_id=123, common_track_id=456'
        )
