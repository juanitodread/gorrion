import argparse

from src.config import Config
from src.clients.spotify import Spotify, SpotifyConfig, SpotifyApiError
from src.clients.twitter import Twitter, TwitterLocal, TwitterConfig
from src.clients.musixmatch import Musixmatch, MusixmatchConfig
from src.gorrion import Gorrion


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

def get_gorrion(local_mode: bool) -> Gorrion:
    spotify = Spotify(Config.get_spotify_config())
    musixmatch = Musixmatch(Config.get_musixmatch_config())

    twitter_config = Config.get_twitter_config()
    twitter = TwitterLocal(twitter_config) if local_mode else Twitter(twitter_config)
    
    return Gorrion(spotify, twitter, musixmatch)

def playing(local_mode: bool) -> None:
    try:
        gorrion = get_gorrion(local_mode)

        tweets = gorrion.playing()
        song, *lyrics = tweets
        
        print('[---------------------- Song -----------------------]')
        print(song.tweet)

        if lyrics:
            lyrics_tweets = '\n\n'.join([lyric.tweet for lyric in lyrics])
            print('[---------------------- Lyric ----------------------]')
            print(lyrics_tweets)
    except SpotifyApiError as error:
        print(error)

if __name__ == "__main__":
    args = parse_args()

    command = args.command
    local_mode = args.local

    valid_commands = ('playing', 'lyric')
    if command not in valid_commands:
        print(f'Invalid command. Use: {valid_commands}')
        quit()

    if command == 'playing':
        playing(local_mode)
    elif command == 'lyric':
        pass