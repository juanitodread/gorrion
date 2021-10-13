from unittest.mock import patch

from src.cli import CLI
from src.clients.twitter import PublishedTweet
from src.clients.spotify import SpotifyApiError


class TestCLI:
    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing.return_value = PublishedTweet('123', 'song', None)

        cli = CLI()
        cli.playing(True)

        print_mock.assert_any_call('[---------------------- Song -----------------------]')
        print_mock.assert_any_call('song')

    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing_when_spotify_error(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing.side_effect = SpotifyApiError('spotify error')

        cli = CLI()
        cli.playing(True)

        print_mock.assert_called()

    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing_with_lyrics(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing_with_lyrics.return_value = [
            PublishedTweet('123', 'song', None),
            PublishedTweet('456', 'song-lyric1', None),
            PublishedTweet('789', 'song-lyric2', None),
        ]

        cli = CLI()
        cli.playing_with_lyrics(True, False)

        print_mock.assert_any_call('[---------------------- Song -----------------------]')
        print_mock.assert_any_call('song')
        print_mock.assert_any_call('[---------------------- Lyric ----------------------]')
        print_mock.assert_any_call('song-lyric1\n\nsong-lyric2')

    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing_with_lyrics_when_spotify_error(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing_with_lyrics.side_effect = SpotifyApiError('spotify error')

        cli = CLI()
        cli.playing_with_lyrics(True, False)

        print_mock.assert_called()

    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing_album(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing_album.return_value = PublishedTweet('123', 'song', None)

        cli = CLI()
        cli.playing_album(True)

        print_mock.assert_any_call('[---------------------- Album ----------------------]')
        print_mock.assert_any_call('song')

    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing_album_when_spotify_error(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing_album.side_effect = SpotifyApiError('spotify error')

        cli = CLI()
        cli.playing_album(True)

        print_mock.assert_called()

    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing_album_with_tracks(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing_album_with_tracks.return_value = [
            PublishedTweet('123', 'album', None),
            PublishedTweet('123', 'track', None),
        ]

        cli = CLI()
        cli.playing_album_with_tracks(True)

        print_mock.assert_any_call('[---------------------- Album ----------------------]')
        print_mock.assert_any_call('album')
        print_mock.assert_any_call('[---------------------- Tracks ---------------------]')
        print_mock.assert_any_call('track')

    @patch('src.cli.Gorrion')
    @patch('builtins.print')
    def test_playing_album_with_tracks_when_spotify_error(self, print_mock, gorrion_mock):
        gorrion_mock.return_value.playing_album_with_tracks.side_effect = SpotifyApiError('spotify error')

        cli = CLI()
        cli.playing_album_with_tracks(True)

        print_mock.assert_called()
