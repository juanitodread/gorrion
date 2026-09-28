from unittest.mock import patch, MagicMock

import pytest
from atproto import client_utils

from src.clients.spotify import SpotifyApiError
from src.clients.twitter import PublishedTweet
from src.clients.bluesky import PublishedPost
from src.config import Config
from src.telegram_bot import TelegramBot


@pytest.fixture()
def event():
    return {
        'message': {
            'from': {
                'username': 'telegram-bot-owner'
            }
        }
    }


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Setup: fill with any logic you want
    owner = Config.TELEGRAM_OWNER_USERNAME
    Config.TELEGRAM_OWNER_USERNAME = 'telegram-bot-owner'

    # this is where the testing happens
    yield

    # Teardown : fill with any logic you want
    Config.TELEGRAM_OWNER_USERNAME = owner


class TestTelegramBot:
    @patch('src.telegram_bot.Bot')
    def test_constructor(self, bot_mock):
        telegram_bot = TelegramBot()

        assert telegram_bot._bot is not None
        bot_mock.assert_called_once_with(token=None)

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_event_when_unknow_sender_event(self, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update

        telegram_bot = TelegramBot()
        telegram_bot.process_event({'event': 'invalid'})

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='Sorry 💔. I can only chat with my creator 🧙🏼.',
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_event_when_telegram_owner_not_set(self, bot_mock, update_mock, event):
        Config.TELEGRAM_OWNER_USERNAME = None

        with pytest.raises(Exception) as error:
            telegram_bot = TelegramBot()
            telegram_bot.process_event(event)

        assert str(error.value) == 'TELEGRAM_OWNER_USERNAME variable is wrong'
        bot_mock.return_value.send_message.assert_not_called()

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_event_when_invalid_command(self, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = 'invalid-command'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

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
                '/album\n'
                '/tracks\n'
                '/about'
            )
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_start_command(self, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/start'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

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
                '/album\n'
                '/tracks\n'
                '/about'
            )
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_command(self, gorrion_mock, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/playing'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing.return_value = [
            'tweet-message',
            PublishedPost(
                cid='cid-123',
                uri='http://uri-123.com',
                post=client_utils.TextBuilder().text(text='post'),
                root_cid='cid-456',
                root_uri='http://uri',
                entity=None,
            ),
        ]

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='post'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_command_when_error(self, gorrion_mock, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/playing'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing.side_effect = SpotifyApiError('error')

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='error'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_command(self, gorrion_mock, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/album'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album.return_value = [
            PublishedTweet(id_='1', tweet='tweet1', entity=None),
            PublishedPost(
                cid='cid-123',
                uri='http://uri-123.com',
                post=client_utils.TextBuilder().text(text='post'),
                root_cid='cid-456',
                root_uri='http://uri',
                entity=None,
            ),
        ]

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='post'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_command_with_error(self, gorrion_mock, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/album'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album.side_effect = SpotifyApiError('error')

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='error'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_with_tracks_command(self, gorrion_mock, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/tracks'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album_with_tracks.return_value = (
            [
                PublishedTweet('123', 'album', None),
                PublishedTweet('123', 'track', None),
            ],
            [
                PublishedPost(
                    cid='cid-123',
                    uri='http://uri-123.com',
                    post=client_utils.TextBuilder().text(text='album'),
                    root_cid='cid-456',
                    root_uri='http://uri',
                    entity=None,
                ),
                PublishedPost(
                    cid='cid-123',
                    uri='http://uri-123.com',
                    post='track',
                    root_cid='cid-456',
                    root_uri='http://uri',
                    entity=None,
                ),
            ],
        )

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='album'
        )
        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='track'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    @patch('src.telegram_bot.Gorrion')
    def test_process_playing_album_with_tracks_command_with_error(self, gorrion_mock, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/tracks'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update
        gorrion_mock.return_value.playing_album_with_tracks.side_effect = SpotifyApiError('error')

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='error'
        )

    @patch('src.telegram_bot.Update')
    @patch('src.telegram_bot.Bot')
    def test_process_about_command(self, bot_mock, update_mock, event):
        update = MagicMock()
        update.message.text = '/about'
        update.message.chat.id = '123'
        update_mock.de_json.return_value = update

        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)

        bot_mock.return_value.send_message.assert_any_call(
            chat_id='123',
            text='Made with ❤️ by @juanitodread'
        )
