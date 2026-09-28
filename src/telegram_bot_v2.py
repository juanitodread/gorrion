import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from src.gorrion import Gorrion
from src.config import Config
from src.clients.spotify import Spotify, NotPlayingError
from src.clients.twitter import TwitterFactory
from src.clients.bluesky import BlueskyFactory
from src.clients.musixmatch import Musixmatch


application = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()


def _new_gorrion(delay_mode: bool) -> Gorrion:
    spotify = Spotify(Config.get_spotify_config())
    musixmatch = Musixmatch(Config.get_musixmatch_config())

    twitter_config = Config.get_twitter_config()
    twitter_config.retweet_delay = delay_mode
    twitter = TwitterFactory.get_client(twitter_config)

    bluesky_config = Config.get_bluesky_config()
    bluesky_config.replay_delay = delay_mode
    bluesky = BlueskyFactory.get_client(bluesky_config)

    return Gorrion(spotify, twitter, bluesky, musixmatch)


class TelegramBot:
    def __init__(self, gorrion: Gorrion) -> None:
        self._gorrion = gorrion
        self._commands = ['/start', '/playing', '/album', '/tracks', '/about']

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._send_message(update, context, 'Welcome to Gorrion Bot 🐦🤖')
        await self._send_message(update, context, f'Supported commands are: \n\n{"\n".join(self._commands)}')

    async def playing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        song = self._gorrion.playing()

        await self._send_message(update, context, song.tweet)

    async def playing_album(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        song = self._gorrion.playing_album()

        await self._send_message(update, context, song.tweet)

    async def playing_album_with_tracks(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        tweets = self._gorrion.playing_album_with_tracks()
        album, *tracks = tweets

        await self._send_message(update, context, album.tweet)

        if tracks:
            for track in tracks:
                await self._send_message(update, context, track.tweet)

    async def about(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._send_message(update, context, 'Made with ❤️ by @juanitodread')

    async def any_other_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        commands = '\n'.join(self._commands)
        await self._send_message(update, context, f'I can only reply to you based on the commands: \n\n{commands}')

    async def _send_message(self, update: Update | object, context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
        if not self._is_bot_owner(update.effective_chat.username):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Sorry 💔. I can only chat with my creator 🧙🏼.'
            )
            return

        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    async def _on_error(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        print(f'Error ({type(context.error)}): {context.error}')

        match context.error:
            case NotPlayingError():
                await self._send_message(update, context, str(context.error))
            case _:
                await self._send_message(update, context, 'Service not available')

    def _is_bot_owner(self, username: str | None) -> bool:
        if not Config.TELEGRAM_OWNER_USERNAME or len(Config.TELEGRAM_OWNER_USERNAME) == 0:
            raise Exception('TELEGRAM_OWNER_USERNAME variable is wrong')

        return Config.TELEGRAM_OWNER_USERNAME == username


def _setup_app(app: Application, bot: TelegramBot) -> Application:
    start_handler = CommandHandler('start', bot.start)
    application.add_handler(start_handler)

    playing_handler = CommandHandler('playing', bot.playing)
    application.add_handler(playing_handler)

    album_handler = CommandHandler('album', bot.playing_album)
    application.add_handler(album_handler)

    tracks_handler = CommandHandler('tracks', bot.playing_album_with_tracks)
    application.add_handler(tracks_handler)

    about_handler = CommandHandler('about', bot.about)
    application.add_handler(about_handler)

    any_other_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), bot.any_other_message)
    application.add_handler(any_other_message_handler)

    application.add_error_handler(bot._on_error)

    return app


def _do_work_local(event, context) -> None:
    gorrion = _new_gorrion(delay_mode=False)
    bot = TelegramBot(gorrion)

    app = _setup_app(application, bot)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


async def _do_work_lambda(event, context) -> dict:
    gorrion = _new_gorrion(delay_mode=False)
    bot = TelegramBot(gorrion)

    app = _setup_app(application, bot)

    try:
        await app.initialize()
        await app.process_update(Update.de_json(event, app.bot))
    except Exception as error:
        print(f'Error: {error}')

    return {
        'status_code': 200,
        'body': {}
    }


def do_work(event, context):
    print(f'Event: {event}')

    # run in lambda
    return asyncio.get_event_loop().run_until_complete(_do_work_lambda(event, context))

    # run in local
    # _do_work_local(event, context)
