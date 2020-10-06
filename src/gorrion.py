import sys
import argparse

from src.config import Config
from src.clients.spotify.client import Spotify
from src.clients.spotify.models import Track
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
        
        status = self.full_status(current_track)

        if len(status) > self._twitter.max_tweet_length:
            print('(Using short status)')
            status = self.short_status(current_track)

        print(status)

        if not disable_twitter:
            post = self._twitter.post(status)
            if post:
                print('Status synced on Twitter')

    def full_status(self, track: Track) -> str:
        return ('Now listening 🔊🎶: \n'
               f'\nTrack: {track.track_number}. {track.name}'
               f'\nAlbum: {track.album.name}'
               f'\nArtist: {", ".join([artist.name for artist in track.artists])}'
               f'\n\n#gorrion #NowPlaying {self.get_artists_hashtag(track.artists)}'
               f'\n\n{track.public_url}')

    def short_status(self, track: Track) -> str:
        return ('Now listening 🔊🎶: \n'
               f'\nTrack: {track.track_number}. {track.name}'
               f'\nAlbum: {track.album.name}'
               f'\nArtist: {", ".join([artist.name for artist in track.artists])}'
               f'\n\n#gorrion #NowPlaying'
               f'\n\n{track.public_url}')

    def get_artists_hashtag(self, artists: list) -> str:
        artists_hashtag = [self.to_hashtag(artist.name) 
                           for artist in artists]
        return ' '.join(artists_hashtag)

    def to_hashtag(self, text: str) -> str:
        words = ''.join(text.split(' '))
        words = words.replace('-', '')
        return f'#{words}'


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
