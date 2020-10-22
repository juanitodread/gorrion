class MusixmatchApiError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ServiceError(MusixmatchApiError):
    def __init__(self, message: str):
        super().__init__(f'Response API error: response="{message}"')


class SongNotFound(MusixmatchApiError):
    def __init__(self, song: str):
        super().__init__(f'Song not found: song={song}')

class LyricNotFound(MusixmatchApiError):
    def __init__(self, track_id: str, common_track_id: str):
        super().__init__(f'Lyric not found. You may try other index: '
                         f'track_id={track_id}, common_track_id={common_track_id}')

class LyricNotProvidedYet(MusixmatchApiError):
    def __init__(self, track_id: str, common_track_id: str):
        super().__init__(f'Lyric not provided for this song or song is instrumental.'
                         f' You may try other index: track_id={track_id}, common_track_id={common_track_id}')
