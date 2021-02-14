from src.clients.spotify.errors import (
    SpotifyApiError,
    ServiceError,
    NotPlayingError,
)


class TestErrors:
    def test_spotify_api_error(self):
        error = SpotifyApiError('error')

        assert str(error) == 'error'

    def test_service_error(self):
        header = {'header1': 'value1'}
        body = {'body1': 'value1'}
        error = ServiceError(header, body)

        assert str(error) == ("Response API error:\n\n"
                              "Reason: {'header': {'header1': 'value1'}, 'body': {'body1': 'value1'}}")

    def test_not_playing_error(self):
        error = NotPlayingError()
        
        assert str(error) == 'Not playing any song at this moment'
