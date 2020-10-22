import re

import requests

from src.clients.musixmatch.models import Song, Track, Lyric
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

    def search_song(self, song: str, artist: str, album: str) -> Song:
        song = Song(song, artist, album)

        response = requests.get(
            f'{Musixmatch.API_URL}/track.search',
            params={
                'q_track': song.name,
                'q_artist': song.artist,
                's_track_rating': 'desc',
                'apikey': self._api_key,
            }
        )

        json_response = response.json()

        status_code = json_response['message']['header']['status_code']

        if status_code != 200:
            if status_code == 404:
                raise SongNotFound(song)
            raise ServiceError(status_code)

        body = json_response['message']['body']

        if body['track_list'] == []:
            raise LyricNotProvidedYet(song)

        tracks = [Track(
                    id_=track['track']['track_id'],
                    common_id=track['track']['commontrack_id'],
                    name=track['track']['track_name'],
                    instrumental=track['track']['instrumental'],
                    explicit=track['track']['explicit'],
                    album=track['track']['album_name'],
                    artist=track['track']['artist_name'],
                ) for track in body['track_list']]

        song.tracks = tracks
        song.tracks_length = len(tracks)

        song.tracks = self._sort_tracks(song)

        return song

    def fetch_lyric(self, song: Song) -> Song:
        for track in song.tracks:
            try:
                lyric = self._fetch_lyric(track.id_, track.common_id)
                song.lyric = lyric
                return song
            except Exception as error:
                print(f'Trying next song: {error}')
                pass
        return song

    def _fetch_lyric(self, track_id: str, common_track_id: str) -> Lyric:
        response = requests.get(
            f'{Musixmatch.API_URL}/track.lyrics.get',
            params={
                'track_id': track_id,
                'commontrack_id': common_track_id,
                'apikey': self._api_key,
            }
        )

        json_response = response.json()

        status_code = json_response['message']['header']['status_code']

        if status_code != 200:
            if status_code == 404:
                raise LyricNotFound(track_id, common_track_id)
            raise ServiceError(status_code)

        body = json_response['message']['body']

        if body == []:
            raise LyricNotProvidedYet(track_id, common_track_id)

        lyric = body['lyrics']

        paragraphs = self._build_lyric(lyric['lyrics_body'])

        return Lyric(
            id_=lyric['lyrics_id'], 
            track_id=track_id,
            common_track_id=common_track_id,
            content=paragraphs
        )

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

    def _sort_tracks(self, song: Song) -> list:        
        # match name and album
        same_albums = []
        diff_albums = []
        for track in song.tracks:
            if track.album and track.album.strip().lower() == song.album.strip().lower():
                same_albums.append(track)
            else:
                diff_albums.append(track)

        return same_albums + diff_albums
