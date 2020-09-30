class SpotifyApiError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ServiceError(SpotifyApiError):
    def __init__(self, message: str):
        super().__init__(f'Response API error: response="{message}"')


class NotPlayingError(SpotifyApiError):
    def __init__(self):
        super().__init__('Not playing any song at this moment')
