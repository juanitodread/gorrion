from json.decoder import JSONDecodeError

import requests

from clients.spotify.models import Track, Album, Artist
from clients.spotify.errors import NotPlayingError


class Spotify:
    API_URL = 'https://api.spotify.com/v1'
    
    def __init__(self, client_token: str) -> None:
        self._client_token = client_token

    def get_current_track(self) -> Track:
        response = requests.get(
            f'{Spotify.API_URL}/me/player/currently-playing',
            headers={
                'Authorization': f'Bearer {self._client_token}'
            }
        )
        
        if response.status_code not in (200, 204):
            raise Exception(f'Error: Response error from Spotify API => {response}')
        
        if response.status_code == 204:
            raise NotPlayingError()

        json_response = response.json()
        
        track = Track(
            id_=json_response['item']['id'],
            name=json_response['item']['name'],
            href=json_response['item']['href'],
            track_number=json_response['item']['track_number'],
            album=Album(
                id_=json_response['item']['album']['id'],
                name=json_response['item']['album']['name'],
                href=json_response['item']['album']['href'],
                release_date=json_response['item']['album']['release_date'],
            ),
            artists=[
                Artist(
                    id_=artist['id'],
                    name=artist['name'],
                    href=artist['href'],
                )
                for artist in json_response['item']['artists']
            ]
        )

        return track
