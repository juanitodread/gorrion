import requests


class Musixmatch:
    API_URL = 'https://api.musixmatch.com/ws/1.1'

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def search_lyric(self, song: str, artist: str) -> str:
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
        body = json_response['message']['body']

        track_id = body['track_list'][0]['track']['track_id']
        common_track_id = body['track_list'][0]['track']['commontrack_id']
        track_name = body['track_list'][0]['track']['track_name']
        album = body['track_list'][0]['track']['album_name']
        artist = body['track_list'][0]['track']['artist_name']

        return (track_id, common_track_id)

    def fetch_lyric(self, track_id: str, common_track_id: str) -> str:
        response = requests.get(
            f'{Musixmatch.API_URL}/track.lyrics.get',
            params={
                'track_id': track_id,
                'commontrack_id': common_track_id,
                'apikey': self._api_key,
            }
        )

        json_response = response.json()
        lyric = json_response['message']['body']['lyrics']['lyrics_body']

        paragraphs = self._build_lyric(lyric)

        return paragraphs

    def _build_lyric(self, raw_lyric: str) -> list:
        # remove metadata text
        lyric = raw_lyric.replace('******* This Lyrics is NOT for Commercial use *******', '')
        lyric = lyric.replace('...', '')

        raw_paragraphs = lyric.split('\n\n')

        # filter paragraphs
        paragraphs = [paragraph for paragraph in raw_paragraphs 
                      if len(paragraph.strip()) > 0]

        return paragraphs
