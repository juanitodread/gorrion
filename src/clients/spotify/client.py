import base64

import requests
from requests import Response

from src.clients.spotify.config import SpotifyConfig
from src.clients.spotify.models import Track, Album, Artist
from src.clients.spotify.errors import ServiceError, NotPlayingError


class Spotify:
    API_URL = 'https://api.spotify.com/v1'
    API_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    API_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

    def __init__(self, config: SpotifyConfig) -> None:
        self._client_id = config.client_id
        self._client_secret = config.client_secret
        self._refresh_token = config.refresh_token

    def get_current_track(self) -> Album:
        token = self._refresh_access_token()
        current_playing_response = self._get_current_playing(token)

        album = self._to_album(current_playing_response['item']['album'])
        album.artists = self._to_artists(current_playing_response['item']['artists'])
        album.tracks = self._to_tracks([current_playing_response['item']])

        return album

    def get_current_album(self) -> Album:
        token = self._refresh_access_token()
        current_playing = self._get_current_playing(token)

        album_id = current_playing['item']['album']['id']

        response = requests.get(
            f'{Spotify.API_URL}/albums/{album_id}',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

        self._verify_spotify_response(response)

        album_response = response.json()

        album = self._to_album(album_response)
        album.artists = self._to_artists(album_response['artists'])
        album.tracks = self._to_tracks(album_response['tracks']['items'])

        return album

    def _get_current_playing(self, token: str) -> dict:
        response = requests.get(
            f'{Spotify.API_URL}/me/player/currently-playing',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

        self._verify_spotify_response(response)

        return response.json()

    def _refresh_access_token(self) -> str:
        authorization = self._get_basic_auth_token()

        response = requests.post(
            Spotify.API_TOKEN_URL,
            headers={
                'Authorization': f'Basic {authorization}'
            },
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self._refresh_token,
            }
        )

        self._verify_spotify_response(response)

        token_response = response.json()

        return token_response['access_token']

    def _verify_spotify_response(self, response: Response) -> None:
        if response.status_code not in (200, 204):
            raise ServiceError(response.headers, response.json())

        if response.status_code == 204:
            raise NotPlayingError()

    def _get_basic_auth_token(self) -> str:
        return self._to_base64(f'{self._client_id}:{self._client_secret}')

    def _to_base64(self, text: str) -> str:
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def _to_album(self, album: dict) -> Album:
        return Album(
            id_=album['id'],
            name=album['name'],
            href=album['href'],
            public_url=album['external_urls']['spotify'],
            release_date=album['release_date'],
            total_tracks=album['total_tracks'],
            artists=[],
            tracks=[],
        )

    def _to_artists(self, artists: list) -> list:
        return [
            Artist(
                id_=artist['id'],
                name=artist['name'],
                href=artist['href'],
                public_url=artist['external_urls']['spotify'],
            ) for artist in artists
        ]

    def _to_tracks(self, tracks: list) -> list:
        return [
            Track(
                id_=track['id'],
                name=track['name'],
                href=track['href'],
                public_url=track['external_urls']['spotify'],
                disc_number=track['disc_number'],
                track_number=track['track_number'],
                duration=track['duration_ms'],
            ) for track in tracks
        ]
