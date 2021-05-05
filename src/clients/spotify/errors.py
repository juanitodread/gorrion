class SpotifyApiError(Exception):
    def __init__(self,
                 message: str,
                 response_header: dict = None,
                 response_body: dict = None):
        if response_header is None and response_body is None:
            super().__init__(message)
            return

        response_header = {} if response_header is None else response_header
        response_body = {} if response_body is None else response_body

        super().__init__(
            f'{message}:\n\nReason: '
            f'{self._build_message(response_header, response_body)}'
        )

    def _build_message(self,
                       response_header: dict,
                       response_body: dict) -> dict:
        return {
            'header': self._remove_token_info(response_header),
            'body': self._remove_token_info(response_body),
        }

    def _remove_token_info(self, content: dict) -> dict:
        return {key: val for key, val in content.items() if 'token' not in key}


class ServiceError(SpotifyApiError):
    def __init__(self, header: dict, body: dict):
        super().__init__('Response API error', header, body)


class NotPlayingError(SpotifyApiError):
    def __init__(self):
        super().__init__('Not playing any song at this moment')
