class NotPlayingError(Exception):
    def __init__(self):
        super().__init__(f'Not playing any song at this moment')
