import sys
import argparse

from src.config import Config
from src.clients.spotify.client import Spotify
from src.clients.twitter.client import Twitter


class Gorrion:
    def __init__(self) -> None:
        self._spotify = Spotify(
            Config.SPOTIFY_CLIENT_ID,
            Config.SPOTIFY_CLIENT_SECRET,
            Config.SPOTIFY_REFRESH_TOKEN,
        )
        self._twitter = Twitter(
            Config.TWITTER_API_CONSUMER_KEY,
            Config.TWITTER_API_CONSUMER_SECRET,
            Config.TWITTER_API_ACCESS_TOKEN,
            Config.TWITTER_API_ACCESS_TOKEN_SECRET,
        )

    def playing(self, disable_twitter: bool=False) -> None:
        current_track = self._spotify.get_current_track()

        current_track_text = ('Now listening 🎶🔊: \n'
                             f'\nTrack: {current_track.track_number}. {current_track.name}'
                             f'\nAlbum: {current_track.album.name}'
                             f'\nArtist: {", ".join([artist.name for artist in current_track.artists])}'
                             '\n\n#gorrion #NowPlaying'
                             f'\n\n{current_track.href.replace("api.spotify.com/v1/tracks", "open.spotify.com/track")}')

        print(current_track_text)

        if not disable_twitter:
            post = self._twitter.post(current_track_text)
            if post:
                print('Status synced on Twitter')


def parse_args():
    parser = argparse.ArgumentParser(description='Gorrion app')
    
    parser.add_argument(
        'command',
        type=str,
        help='The available commands to execute: [playing, lyric].'
    )
    parser.add_argument(
        '-l',
        '--local',
        action='store_true',
        default=False,
        help='Enables local mode. No Twitter sync.'
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    command = args.command
    local_mode = args.local

    valid_commands = ('playing', 'lyric')
    if command not in valid_commands:
        print(f'Invalid command. Use: {valid_commands}')
        quit()

    gorrion = Gorrion()
    if command == 'playing':
        gorrion.playing(local_mode)
    elif command == 'lyric':
        pass
