import argparse

from src.config import Config
from src.clients.spotify import Spotify, SpotifyApiError
from src.clients.twitter import Twitter, TwitterLocal
from src.clients.musixmatch import Musixmatch
from src.gorrion import Gorrion


class CLI:
    def playing(self, local_mode: bool) -> None:
        try:
            gorrion = self._build_gorrion(local_mode, False)

            song = gorrion.playing()

            print(self._get_song_header())
            print(song.tweet)
        except SpotifyApiError as error:
            print(error)

    def playing_with_lyrics(self, local_mode: bool, delay_mode: bool) -> None:
        try:
            gorrion = self._build_gorrion(local_mode, delay_mode)

            tweets = gorrion.playing_with_lyrics()
            song, *lyrics = tweets

            print(self._get_song_header())
            print(song.tweet)

            if lyrics:
                lyrics_tweets = '\n\n'.join([lyric.tweet for lyric in lyrics])
                print(self._get_lyric_header())
                print(lyrics_tweets)
        except SpotifyApiError as error:
            print(error)

    def _build_gorrion(self, local_mode: bool, delay_mode: bool) -> Gorrion:
        spotify = Spotify(Config.get_spotify_config())
        musixmatch = Musixmatch(Config.get_musixmatch_config())

        twitter_config = Config.get_twitter_config()
        twitter_config.retweet_delay = delay_mode
        twitter = TwitterLocal(twitter_config) if local_mode else Twitter(twitter_config)

        return Gorrion(spotify, twitter, musixmatch)

    def _get_song_header(self) -> str:
        return '[---------------------- Song -----------------------]'

    def _get_lyric_header(self) -> str:
        return '[---------------------- Lyric ----------------------]'

    def _parse_args(self) -> None:
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
        parser.add_argument(
            '-d',
            '--delay',
            action='store_true',
            default=False,
            help='Enables lyric delay mode.'
        )

        return parser.parse_args()


if __name__ == "__main__":
    cli = CLI()
    args = cli._parse_args()

    command = args.command
    local_mode = args.local
    delay_mode = args.delay

    valid_commands = ('playing', 'lyric')
    if command not in valid_commands:
        print(f'Invalid command. Use: {valid_commands}')
        quit()

    if command == 'playing':
        cli.playing(local_mode)
        quit()
    if command == 'lyric':
        cli.playing_with_lyrics(local_mode, delay_mode)
        quit()
