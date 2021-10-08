from src.clients.spotify import (
    Spotify,
    Album,
)
from src.clients.twitter import (
    Twitter,
    PublishedTweet,
)
from src.clients.musixmatch import (
    Musixmatch,
    Song,
    MusixmatchApiError,
)
from src.templates import (
    TweetTemplate,
    TweetConfig,
    TweetSongConfig,
    TweetAlbumConfig,
)


class Gorrion:
    def __init__(self,
                 spotify: Spotify,
                 twitter: Twitter,
                 musixmatch: Musixmatch) -> None:
        self._spotify = spotify
        self._twitter = twitter
        self._musixmatch = musixmatch

    def playing(self) -> PublishedTweet:
        current_album = self.get_playing_album()
        tweet = self.publish_track(current_album)

        return tweet

    def playing_with_lyrics(self) -> list:
        current_album_tweet = self.playing()

        song = self.get_lyric(current_album_tweet.entity)
        lyrics_tweets = self.publish_lyrics(current_album_tweet, song)

        return [current_album_tweet, *lyrics_tweets]

    def playing_album(self) -> PublishedTweet:
        current_album = self.get_playing_album()
        tweet = self.publish_album(current_album)

        return tweet

    def get_playing_album(self) -> Album:
        current_album = self._spotify.get_current_track()
        return current_album

    def get_lyric(self, album: Album) -> Song:
        song = Song(
            album.tracks[0].name,
            album.artists[0].name,
            album.name,
        )

        try:
            song = self._musixmatch.search_song(song)
            song = self._musixmatch.fetch_lyric(song)
        except MusixmatchApiError:
            pass

        return song

    def publish_track(self, album: Album) -> PublishedTweet:
        tweet_track = self.build_status(album, TweetSongConfig())
        tweeted_track = self._twitter.post(tweet_track)
        tweeted_track.entity = album

        return tweeted_track

    def publish_lyrics(self,
                       tweeted_track: PublishedTweet,
                       song: Song) -> list:
        if not song.lyric:
            return []

        tweet = tweeted_track
        published_tweets = []
        lyrics = self.lyrics_to_tweets(song.lyric.content)

        for lyric in lyrics:
            tweet = self._twitter.reply(lyric, tweet.id_)
            published_tweets.append(tweet)

        return published_tweets

    def publish_album(self, album: Album) -> PublishedTweet:
        tweet_album = self.build_status(album, TweetAlbumConfig())

        tweeted_album = self._twitter.post(tweet_album)
        tweeted_album.entity = album

        return tweeted_album

    def build_status(self, album: Album, config: TweetConfig):
        template = TweetTemplate(album, config)
        tweet_status = template.to_tweet()

        if not self.is_valid_tweet_status(tweet_status):
            config.footer_config.with_artists_hashtag = False
            template = TweetTemplate(album, config)
            tweet_status = template.to_tweet()

        return tweet_status

    def is_valid_tweet_status(self, status: str) -> bool:
        return len(status) <= self._twitter.max_tweet_length

    def lyrics_to_tweets(self, lyrics: list) -> list:
        lyric_tweets = []
        for paragraph in lyrics:
            if self.is_valid_tweet_status(paragraph):
                lyric_tweets.append(paragraph)
            else:
                lines = paragraph.split('\n')
                lines_group = self._chunks(lines, 4)
                new_paragraphs = ['\n'.join(new_paragraph)
                                  for new_paragraph in lines_group]
                lyric_tweets += new_paragraphs

        return lyric_tweets

    def _chunks(self, elements: list, size: int) -> list:
        return [elements[element:element + size]
                for element in range(0, len(elements), size)]
