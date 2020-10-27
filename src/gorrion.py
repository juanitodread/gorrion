import sys
import argparse
import time

from src.config import Config
from src.clients.spotify.client import Spotify
from src.clients.spotify.models import Track
from src.clients.twitter.client import Twitter
from src.clients.musixmatch.client import Musixmatch


class Gorrion:
    def __init__(self) -> None:
        self._spotify = Spotify(Config.get_spotify_config())
        self._twitter = Twitter(Config.get_twitter_config())
        self._musixmatch = Musixmatch(Config.get_musixmatch_config())

    def playing(self, disable_twitter: bool=False) -> None:
        current_track = self._spotify.get_current_track()
        
        status = self.full_status(current_track)

        if not self.is_valid_tweet_status(status):
            print('(Using short status)')
            status = self.short_status(current_track)

        print(status)

        song = self._musixmatch.search_song(
            current_track.name,
            current_track.artists[0].name,
            current_track.album.name
        )
        song = self._musixmatch.fetch_lyric(song)
        lyric_tweets = self.lyrics_to_tweets(song.lyric.content)

        print('\n[---------------------- Lyric ----------------------]')
        if not disable_twitter:
            post = self._twitter.post(status)
            if post:
                print('Status synced on Twitter')
            
            for tweet in lyric_tweets:
                print(f'{tweet}\n')
                post = self._twitter.reply(tweet, post.id)
        else:
            for tweet in lyric_tweets:
                print(f'{tweet}\n')

    def full_status(self, track: Track) -> str:
        return ('Now listening 🔊🎶: \n'
               f'\nTrack: {track.track_number}. {track.name}'
               f'\nAlbum: {track.album.name}'
               f'\nArtist: {", ".join([artist.name for artist in track.artists])}'
               f'\n\n#gorrion #NowPlaying {self.get_artists_hashtag(track.artists)}'
               f'\n\n{track.href.replace("api.spotify.com/v1/tracks", "open.spotify.com/track")}')

    def short_status(self, track: Track) -> str:
        return ('Now listening 🔊🎶: \n'
               f'\nTrack: {track.track_number}. {track.name}'
               f'\nAlbum: {track.album.name}'
               f'\nArtist: {", ".join([artist.name for artist in track.artists])}'
               f'\n\n#gorrion #NowPlaying'
               f'\n\n{track.href.replace("api.spotify.com/v1/tracks", "open.spotify.com/track")}')

    def get_artists_hashtag(self, artists: list) -> str:
        artists_hashtag = [self.to_hashtag(artist.name) 
                           for artist in artists]
        return ' '.join(artists_hashtag)

    def to_hashtag(self, text: str) -> str:
        words = ''.join(text.split(' '))
        words = words.replace('-', '')
        return f'#{words}'

    def is_valid_tweet_status(self, status: str) -> bool:
        return len(status) <= self._twitter.max_tweet_length

    def lyrics_to_tweets(self, lyrics: list) -> list:
        lyric_tweets = []
        for paragraph in lyrics:
            if self.is_valid_tweet_status(paragraph):
                lyric_tweets.append(paragraph)
            else:
                lines = paragraph.split('\n')
                lines_group = self.chunks(lines, 4)
                new_paragraphs = ['\n'.join(new_paragraph) for new_paragraph in lines_group]
                lyric_tweets += new_paragraphs

        return lyric_tweets

    def chunks(self, elements: list, size: int) -> list:
        return [elements[element:element + size]
                for element in range(0, len(elements), size)]



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
