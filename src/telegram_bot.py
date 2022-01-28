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

        self._check_event(event, chat_id, text)

        try:
            gorrion = self._build_gorrion(False, False)
            if text == '/playing':
                self.playing(chat_id, gorrion)
                return
            if text == '/lyric':
                self.playing_with_lyrics(chat_id, gorrion)
                return
            if text == '/album':
                self.playing_album(chat_id, gorrion)
                return
            if text == '/tracks':
                self.playing_album_with_tracks(chat_id, gorrion)
                return
        except SpotifyApiError as error:
            self._bot.send_message(
                chat_id=chat_id,
                text=f'{error}',
            )

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

    def playing(self, chat_id: str, gorrion: Gorrion) -> None:
        song = gorrion.playing()

        self._bot.send_message(
            chat_id=chat_id,
            text=song.tweet
        )

    def playing_with_lyrics(self, chat_id: str, gorrion: Gorrion) -> None:
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

    def playing_album(self, chat_id: str, gorrion: Gorrion) -> None:
        song = gorrion.playing_album()

        self._bot.send_message(
            chat_id=chat_id,
            text=song.tweet
        )

    def playing_album_with_tracks(self, chat_id: str, gorrion: Gorrion) -> None:
        tweets = gorrion.playing_album_with_tracks()
        album, *tracks = tweets

        self._bot.send_message(
            chat_id=chat_id,
            text=album.tweet
        )

        if tracks:
            for track in tracks:
                self._bot.send_message(
                    chat_id=chat_id,
                    text=track.tweet
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

    def invalid_sender(self, chat_id: str) -> None:
        self._bot.send_message(
            chat_id=chat_id,
            text='Sorry 💔. I can only chat with my creator 🧙🏼.'
        )

    def _build_gorrion(self, local_mode: bool, delay_mode: bool) -> Gorrion:
        spotify = Spotify(Config.get_spotify_config())
        musixmatch = Musixmatch(Config.get_musixmatch_config())

        twitter_config = Config.get_twitter_config()
        twitter_config.retweet_delay = delay_mode
        twitter = (TwitterLocal(twitter_config)
                   if local_mode else Twitter(twitter_config))

        return Gorrion(spotify, twitter, musixmatch)

    def _check_event(self, event: dict, chat_id: str, text: str) -> None:
        if not self._is_telegram_owner_sending(event):
            self.invalid_sender(chat_id)
            return

        if text not in self._get_commands():
            self.invalid_command(chat_id)
            return

        if text == '/start':
            self.start(chat_id)
            return

        if text == '/about':
            self.about(chat_id)
            return

    def _get_commands(self) -> list:
        return ['/start', '/playing', '/lyric', '/album', '/tracks', '/about']

    def _is_telegram_owner_sending(self, event: dict) -> bool:
        if not Config.TELEGRAM_OWNER_USERNAME:
            raise Exception('TELEGRAM_OWNER_USERNAME variable is wrong')

        return Config.TELEGRAM_OWNER_USERNAME == event.get('message', {}).get('from', {}).get('username', '')


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
