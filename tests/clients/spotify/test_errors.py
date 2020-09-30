from src.clients.spotify.errors import SpotifyApiError, ServiceError, NotPlayingError


class TestErrors:
    def test_spotify_api_error(self):
        error = SpotifyApiError('error')

        assert str(error) == 'error'

    def test_service_error(self):
        error = ServiceError('service-error')

        assert str(error) == 'Response API error: response="service-error"'

    def test_not_playing_error(self):
        error = NotPlayingError()
        
        assert str(error) == 'Not playing any song at this moment'
