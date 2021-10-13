import argparse
from argparse import Namespace

from src.config import Config
from src.clients.spotify import Spotify, SpotifyApiError
from src.clients.twitter import Twitter, TwitterLocal
from src.clients.musixmatch import Musixmatch
from src.gorrion import Gorrion


class CLI:
    COMMANDS = ('playing', 'lyric', 'album', 'album-tracks')

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

    def playing_album(self, local_mode: bool) -> None:
        try:
            gorrion = self._build_gorrion(local_mode, False)

            song = gorrion.playing_album()

            print(self._get_album_header())
            print(song.tweet)
        except SpotifyApiError as error:
            print(error)

    def playing_album_with_tracks(self, local_mode: bool) -> None:
        try:
            gorrion = self._build_gorrion(local_mode, False)

            tweets = gorrion.playing_album_with_tracks()
            album, *tracks = tweets

            print(self._get_album_header())
            print(album.tweet)

            if tracks:
                tracks_tweets = '\n'.join([track.tweet for track in tracks])
                print(self._get_track_header())
                print(tracks_tweets)
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

    def _get_album_header(self) -> str:
        return '[---------------------- Album ----------------------]'

    def _get_track_header(self) -> str:
        return '[---------------------- Tracks ---------------------]'

    def _parse_args(self) -> Namespace:
        parser = argparse.ArgumentParser(description='Gorrion app')

        parser.add_argument(
            'command',
            type=str,
            help=f'The available commands to execute: {CLI.COMMANDS}.'
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

    if command not in CLI.COMMANDS:
        print(f'Invalid command. Use: {CLI.COMMANDS}')
        quit()
    if command == 'playing':
        cli.playing(local_mode)
        quit()
    if command == 'lyric':
        cli.playing_with_lyrics(local_mode, delay_mode)
        quit()
    if command == 'album':
        cli.playing_album(local_mode)
        quit()
    if command == 'album-tracks':
        cli.playing_album_with_tracks(local_mode)
        quit()
