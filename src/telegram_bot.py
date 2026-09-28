from telegram import Bot, Update

from src.gorrion import Gorrion
from src.config import Config
from src.clients.spotify import Spotify, SpotifyApiError
from src.clients.twitter import TwitterFactory
from src.clients.bluesky import BlueskyFactory
from src.clients.musixmatch import Musixmatch


class TelegramBot:
    def __init__(self) -> None:
        self._bot = Bot(token=Config.TELEGRAM_TOKEN)

    def process_event(self, event: dict) -> None:
        update = Update.de_json(event, self._bot)

        chat_id = update.message.chat.id
        text = update.message.text.encode('utf-8').decode()

        if not self._is_event_valid(event, chat_id, text):
            return

        try:
            gorrion = self._build_gorrion(False)
            if text == '/playing':
                self.playing(chat_id, gorrion)
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
        [song, bluesky_song] = gorrion.playing()

        self._bot.send_message(
            chat_id=chat_id,
            text=bluesky_song.post.build_text()
        )

    def playing_album(self, chat_id: str, gorrion: Gorrion) -> None:
        [album, bluesky_album] = gorrion.playing_album()

        self._bot.send_message(
            chat_id=chat_id,
            text=bluesky_album.post.build_text()
        )

    def playing_album_with_tracks(self, chat_id: str, gorrion: Gorrion) -> None:
        [tweets, bluesky] = gorrion.playing_album_with_tracks()
        album, *tracks = bluesky

        self._bot.send_message(
            chat_id=chat_id,
            text=album.post.build_text()
        )

        tracks_tweets = '\n'.join([track.post for track in tracks])
        self._bot.send_message(
            chat_id=chat_id,
            text=tracks_tweets
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

    def _build_gorrion(self, delay_mode: bool) -> Gorrion:
        spotify = Spotify(Config.get_spotify_config())
        musixmatch = Musixmatch(Config.get_musixmatch_config())

        twitter_config = Config.get_twitter_config()
        twitter_config.retweet_delay = delay_mode
        twitter = TwitterFactory.get_client(twitter_config)

        bluesky_config = Config.get_bluesky_config()
        bluesky_config.replay_delay = delay_mode
        bluesky = BlueskyFactory.get_client(bluesky_config)

        return Gorrion(spotify, twitter, bluesky, musixmatch)

    def _is_event_valid(self, event: dict, chat_id: str, text: str) -> bool:
        if not self._is_telegram_owner_sending(event):
            self.invalid_sender(chat_id)
            return False

        if text not in self._get_commands():
            self.invalid_command(chat_id)
            return False

        if text == '/start':
            self.start(chat_id)
            return False

        if text == '/about':
            self.about(chat_id)
            return False

        return True

    def _get_commands(self) -> list:
        return ['/start', '/playing', '/album', '/tracks', '/about']

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
