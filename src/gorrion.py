from atproto_client.utils import TextBuilder
from tweet_counter import count_tweet

from src.clients.spotify import (
    Spotify,
    Album,
    Track,
)
from src.clients.twitter import (
    Twitter,
    PublishedTweet,
)
from src.clients.bluesky import (
    Bluesky,
    PublishedPost,
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
    BlueskyTemplate,
)


class Gorrion:
    def __init__(self,
                 spotify: Spotify,
                 twitter: Twitter,
                 bluesky: Bluesky,
                 musixmatch: Musixmatch) -> None:
        self._spotify = spotify
        self._twitter = twitter
        self._bluesky = bluesky
        self._musixmatch = musixmatch

    def playing(self) -> tuple[PublishedTweet, PublishedPost]:
        current_album = self._spotify.get_current_track()

        published_tweet = self.publish_track(current_album)
        published_post = self.publish_track_to_bluesky(current_album)

        return published_tweet, published_post

    def playing_with_lyrics(self) -> list:
        [current_album_tweet, _] = self.playing()

        song = self.get_lyric(current_album_tweet.entity)
        lyrics_tweets = self.publish_lyrics(current_album_tweet, song)

        return [current_album_tweet, *lyrics_tweets]

    def playing_album(self) -> tuple[PublishedTweet, PublishedPost]:
        current_album = self._spotify.get_current_track()

        published_tweet = self.publish_album(current_album)
        published_post = self.publish_album_to_bluesky(current_album)

        return published_tweet, published_post

    def playing_album_with_tracks(self) -> tuple[list, list]:
        album = self._spotify.get_current_album()

        twitter_album = self.publish_album(album)
        bluesky_album = self.publish_album_to_bluesky(album)

        twitter_tracks = self.publish_tracks(twitter_album)
        bluesky_tracks = self.publish_tracks_to_bluesky(bluesky_album)

        return [twitter_album, *twitter_tracks], [bluesky_album, *bluesky_tracks]

    def get_lyric(self, album: Album) -> Song:
        song = Song(
            album.tracks[0].name,
            album.artists[0].name,
            album.name,
        )

        # Musixmatch no longer supports free API calls.
        return song

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

    def publish_track_to_bluesky(self, album: Album) -> PublishedPost:
        bluesky_post = self.build_bluesky_status(album, TweetSongConfig())
        posted_post = self._bluesky.post(bluesky_post)
        posted_post.entity = album

        return posted_post

    def publish_lyrics(self, tweeted_track: PublishedTweet, song: Song) -> list:
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

    def publish_album_to_bluesky(self, album: Album) -> PublishedPost:
        bluesky_post = self.build_bluesky_status(album, TweetAlbumConfig())
        posted_post = self._bluesky.post(bluesky_post)
        posted_post.entity = album

        return posted_post

    def publish_tracks(self, tweeted_album: PublishedTweet) -> list:
        album = tweeted_album.entity

        tweet = tweeted_album
        published_tweets = []
        tracks = self._tracks_to_tweets(album.tracks)

        for track in tracks:
            tweet = self._twitter.reply(track, tweet.id_)
            published_tweets.append(tweet)

        return published_tweets

    def publish_tracks_to_bluesky(self, posted_album: PublishedPost) -> list:
        album = posted_album.entity
        post = posted_album
        published_posts = []
        tracks = self._tracks_to_tweets(album.tracks)
        for track in tracks:
            post = self._bluesky.reply(track, post)
            published_posts.append(post)
        return published_posts

    def build_status(self, album: Album, config: TweetConfig):
        template = TweetTemplate(album, config)
        tweet_status = template.to_tweet()

        if not self.is_valid_tweet_status(tweet_status):
            config.footer_config.with_artists_hashtag = False
            template = TweetTemplate(album, config)
            tweet_status = template.to_tweet()

        return tweet_status

    def build_bluesky_status(self, album: Album, config: TweetConfig) -> TextBuilder:
        template = BlueskyTemplate(album, config)
        tweet_status = template.to_tweet()

        if not self.is_valid_bluesky_post_status(tweet_status):
            config.footer_config.with_artists_hashtag = False
            template = TweetTemplate(album, config)
            tweet_status = template.to_tweet()

        return tweet_status

    def is_valid_tweet_status(self, status: str) -> bool:
        return count_tweet(status) <= self._twitter.max_tweet_length

    def is_valid_bluesky_post_status(self, status: TextBuilder) -> bool:
        return len(status.build_text()) <= self._bluesky.max_post_length

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

    def _tracks_to_tweets(self, tracks: list) -> list:
        track_tweets = []

        tweet = ''
        for track in tracks:
            tweet_content = self._track_to_tweet(track)
            if self.is_valid_tweet_status(tweet + tweet_content + '\n'):
                tweet += tweet_content + '\n'
            else:
                track_tweets.append(tweet)
                tweet = tweet_content + '\n'

        if tweet:
            track_tweets.append(tweet)

        track_tweets[-1] = track_tweets[-1].strip()

        return track_tweets

    def _track_to_tweet(self, track: Track) -> str:
        return f'{track.disc_number}.{track.track_number}) {track.name} {self._format_duration(track.duration)}'

    def _format_duration(self, duration: int) -> str:
        seconds = int((duration / 1000) % 60)
        minutes = int((duration / (1000 * 60)) % 60)

        return f'⏳{minutes}:{seconds:02d}'

    def _chunks(self, elements: list, size: int) -> list:
        return [elements[element:element + size]
                for element in range(0, len(elements), size)]
