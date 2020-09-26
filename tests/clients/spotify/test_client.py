from src.clients.spotify.client import Spotify


class TestSpotify:
    def test_constructor(self):
        spotify = Spotify('client_id', 'client_secret', 'refresh_token')
        
        assert spotify._client_id == 'client_id'
        assert spotify._client_secret == 'client_secret'
        assert spotify._refresh_token == 'refresh_token'
