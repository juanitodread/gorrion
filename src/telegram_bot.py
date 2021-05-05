from telegram import Bot, Update

from src.gorrion import Gorrion
from src.config import Config
from src.clients.spotify import Spotify, SpotifyApiError
from src.clients.twitter import Twitter, TwitterLocal
from src.clients.musixmatch import Musixmatch


class TelegramBot:
    def __init__(self) -> None:
        self._bot = Bot(token=Config.TELEGRAM_TOKEN)

    def process_event(self, event: dict) -> None:
        update = Update.de_json(event, self._bot)

        chat_id = update.message.chat.id
        text = update.message.text.encode('utf-8').decode()

        if text not in self._get_commands():
            self.invalid_command(chat_id)
            return

        if text == '/start':
            self.start(chat_id)
            return
        if text == '/playing':
            self.playing(chat_id, False)
            return
        if text == '/lyric':
            self.playing_with_lyrics(chat_id, False, False)
            return
        if text == '/about':
            self.about(chat_id)
            return

    def start(self, chat_id: str) -> None:
        self._bot.send_message(
            chat_id=chat_id,
            text='Welcome to Gorrion Bot 🐦🤖'
        )
        commands = '\n'.join(self._get_commands())
        self._bot.send_message(
            chat_id=chat_id,
            text=f'Supported commands are: \n\n{commands}',
        )

    def playing(self, chat_id: str, local_mode: bool) -> None:
        try:
            gorrion = self._build_gorrion(local_mode, False)

            song = gorrion.playing()

            self._bot.send_message(
                chat_id=chat_id,
                text=song.tweet
            )
        except SpotifyApiError as error:
            self._bot.send_message(
                chat_id=chat_id,
                text=f'{error}',
            )

    def playing_with_lyrics(self,
                            chat_id: str,
                            local_mode: bool,
                            delay_mode: bool) -> None:
        try:
            gorrion = self._build_gorrion(local_mode, delay_mode)

            tweets = gorrion.playing_with_lyrics()
            song, *lyrics = tweets

            self._bot.send_message(
                chat_id=chat_id,
                text=song.tweet
            )
            if lyrics:
                for lyric in lyrics:
                    self._bot.send_message(
                        chat_id=chat_id,
                        text=lyric.tweet
                    )
        except SpotifyApiError as error:
            self._bot.send_message(
                chat_id=chat_id,
                text=f'{error}',
            )

    def about(self, chat_id: str) -> None:
        self._bot.send_message(
            chat_id=chat_id,
            text='Made with ❤️ by @juanitodread'
        )

    def invalid_command(self, chat_id: str) -> None:
        self._bot.send_message(
            chat_id=chat_id,
            text='Invalid command'
        )
        commands = '\n'.join(self._get_commands())
        self._bot.send_message(
            chat_id=chat_id,
            text=f'Supported commands are: \n\n{commands}'
        )

    def _build_gorrion(self, local_mode: bool, delay_mode: bool) -> Gorrion:
        spotify = Spotify(Config.get_spotify_config())
        musixmatch = Musixmatch(Config.get_musixmatch_config())

        twitter_config = Config.get_twitter_config()
        twitter_config.retweet_delay = delay_mode
        twitter = TwitterLocal(twitter_config) if local_mode else Twitter(twitter_config)

        return Gorrion(spotify, twitter, musixmatch)

    def _get_commands(self) -> list:
        return ['/start', '/playing', '/lyric', '/about']


def do_work(event, context) -> dict:
    try:
        print('EVENT', event)
        telegram_bot = TelegramBot()
        telegram_bot.process_event(event)
    except Exception as error:
        print('ERROR', error)

    return {
        'status_code': 200,
        'body': {}
    }
