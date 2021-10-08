import base64

import requests

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

    def refresh_access_token(self) -> str:
        authorization = self.get_basic_auth_token()

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

        if response.status_code != 200:
            raise ServiceError(response.headers, response.json())

        json_response = response.json()

        return json_response['access_token']

    def get_current_track(self) -> Album:
        access_token = self.refresh_access_token()

        response = requests.get(
            f'{Spotify.API_URL}/me/player/currently-playing',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if response.status_code not in (200, 204):
            raise ServiceError(response.headers, response.json())

        if response.status_code == 204:
            raise NotPlayingError()

        json_response = response.json()

        album = Album(
            id_=json_response['item']['album']['id'],
            name=json_response['item']['album']['name'],
            href=json_response['item']['album']['href'],
            public_url=json_response['item']['album']['external_urls']['spotify'],
            release_date=json_response['item']['album']['release_date'],
            total_tracks=json_response['item']['album']['total_tracks'],
            artists=[
                Artist(
                    id_=artist['id'],
                    name=artist['name'],
                    href=artist['href'],
                    public_url=artist['external_urls']['spotify'],
                )
                for artist in json_response['item']['artists']
            ],
            tracks=[
                Track(
                    id_=json_response['item']['id'],
                    name=json_response['item']['name'],
                    href=json_response['item']['href'],
                    public_url=json_response['item']['external_urls']['spotify'],
                    disc_number=json_response['item']['disc_number'],
                    track_number=json_response['item']['track_number'],
                    duration=json_response['item']['duration_ms'],
                ),
            ],
        )

        return album

    def get_current_album(self) -> Album:
        access_token = self.refresh_access_token()

        response = requests.get(
            f'{Spotify.API_URL}/me/player/currently-playing',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if response.status_code not in (200, 204):
            raise ServiceError(response.headers, response.json())

        if response.status_code == 204:
            raise NotPlayingError()

        json_response = response.json()

        album_id = json_response['item']['album']['id']
        album_response = requests.get(
            f'{Spotify.API_URL}/albums/{album_id}',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if album_response.status_code not in (200, 204):
            raise ServiceError(album_response.headers, response.json())

        if response.status_code == 204:
            raise NotPlayingError()

        album_json_response = album_response.json()

        album = Album(
            id_=album_json_response['id'],
            name=album_json_response['name'],
            href=album_json_response['href'],
            public_url=album_json_response['external_urls']['spotify'],
            release_date=album_json_response['release_date'],
            total_tracks=album_json_response['total_tracks'],
            artists=[
                Artist(
                    id_=artist['id'],
                    name=artist['name'],
                    href=artist['href'],
                    public_url=artist['external_urls']['spotify'],
                )
                for artist in album_json_response['artists']
            ],
            tracks=[
                Track(
                    id_=track['id'],
                    name=track['name'],
                    href=track['href'],
                    public_url=track['external_urls']['spotify'],
                    disc_number=track['disc_number'],
                    track_number=track['track_number'],
                    duration=track['duration_ms'],
                )
                for track in album_json_response['tracks']['items']
            ]
        )

        return album

    def get_basic_auth_token(self) -> str:
        return self.to_base64(f'{self._client_id}:{self._client_secret}')

    def to_base64(self, text: str) -> str:
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
