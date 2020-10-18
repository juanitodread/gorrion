import re

import requests

from src.clients.musixmatch.errors import (
    SongNotFound,
    ServiceError,
    LyricNotFound,
    LyricNotProvidedYet,
)


class Musixmatch:
    API_URL = 'https://api.musixmatch.com/ws/1.1'

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def search_song(self, song: str, artist: str) -> str:
        response = requests.get(
            f'{Musixmatch.API_URL}/track.search',
            params={
                'q_track': song,
                'q_artist': artist,
                's_track_rating': 'desc',
                'apikey': self._api_key,
            }
        )

        json_response = response.json()

        status_code = json_response['message']['header']['status_code']

        if status_code != 200:
            if status_code == 404:
                raise SongNotFound(song, artist)
            raise ServiceError(status_code)

        body = json_response['message']['body']
        track = body['track_list'][0]['track']

        track_id = track['track_id']
        common_track_id = track['commontrack_id']

        return (track_id, common_track_id)

    def fetch_lyric(self, track_id: str, common_track_id: str) -> list:
        response = requests.get(
            f'{Musixmatch.API_URL}/track.lyrics.get',
            params={
                'track_id': track_id,
                'commontrack_id': common_track_id,
                'apikey': self._api_key,
            }
        )

        json_response = response.json()

        print('JSON', json_response)

        status_code = json_response['message']['header']['status_code']

        if status_code != 200:
            if status_code == 404:
                raise LyricNotFound(track_id, common_track_id)
            raise ServiceError(status_code)

        body = json_response['message']['body']

        if body == []:
            raise LyricNotProvidedYet(track_id, common_track_id)

        lyric = body['lyrics']['lyrics_body']

        paragraphs = self._build_lyric(lyric)

        return paragraphs

    def _build_lyric(self, raw_lyric: str) -> list:
        # remove metadata text
        lyric = raw_lyric.replace('******* This Lyrics is NOT for Commercial use *******', '')
        lyric = lyric.replace('...', '')
        lyric = re.sub(r'\([0-9]+\)', '', lyric)

        raw_paragraphs = lyric.split('\n\n')

        # filter paragraphs
        paragraphs = [paragraph for paragraph in raw_paragraphs 
                      if len(paragraph.strip()) > 0]

        return paragraphs
