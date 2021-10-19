from unittest.mock import patch, MagicMock

from src.clients.spotify import SpotifyApiError
from src.clients.twitter import PublishedTweet
from src.telegram_bot import TelegramBot


class TestTelegramBot:
    @patch('src.telegram_bot.Bot')
    def test_constructor(self, bot_mock):
        telegram_bot = TelegramBot()

        assert telegram_bot._bot is not None
        bot_mock.assert_called_once_with(token=None)

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_event_when_invalid_command(self, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = 'invalid-command'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='Invalid command',
        )
        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text=(
                'Supported commands are: \n\n'
                '/start\n'
                '/playing\n'
                '/lyric\n'
                '/album\n'
                '/tracks\n'
                '/about'
            )
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_start_command(self, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/start'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='Welcome to Gorrion Bot 🐦🤖'
        )
        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text=(
                'Supported commands are: \n\n'
                '/start\n'
                '/playing\n'
                '/lyric\n'
                '/album\n'
                '/tracks\n'
                '/about'
            )
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_command(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/playing'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing.return_value.tweet = 'tweet-message'

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='tweet-message'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_command_when_error(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/playing'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing.side_effect = SpotifyApiError('error')

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='error'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_with_lyrics_command(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/lyric'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_with_lyrics.return_value = [
            PublishedTweet(id_='1', tweet='tweet1', entity=None),
            PublishedTweet(id_='2', tweet='lyric1', entity=None),
        ]

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='tweet1'
        )
        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='lyric1'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_with_lyrics_command_when_error(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/lyric'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_with_lyrics.side_effect = SpotifyApiError('error')

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='error'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_command(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/album'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album.return_value = PublishedTweet(id_='1', tweet='tweet1', entity=None)

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='tweet1'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_command_with_error(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/album'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album.side_effect = SpotifyApiError('error')

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='error'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_with_tracks_command(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/tracks'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album_with_tracks.return_value = [
            PublishedTweet(id_='1', tweet='album-tweet', entity=None),
            PublishedTweet(id_='2', tweet='tracks-tweet', entity=None),
        ]

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='album-tweet'
        )
        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='tracks-tweet'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_with_tracks_command_with_error(self, gorrion_mock, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/tracks'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album_with_tracks.side_effect = SpotifyApiError('error')

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='error'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_about_command(self, bot_mock, update_mock):
        update = MagicMock()
        update.message.text = '/about'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update

        telegram_bot = TelegramBot()
        telegram_bot.process_event({})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='Made with ❤️ by @juanitodread'
        )
