from src.config import Config
from src.clients.spotify.client import Spotify


class Gorrion:
    def run(self):
        spotify = Spotify(
            Config.SPOTIFY_CLIENT_ID,
            Config.SPOTIFY_CLIENT_SECRET,
            Config.SPOTIFY_REFRESH_TOKEN,
        )

        current_track = spotify.get_current_track()
        print('CURRENT_TRACK: ', current_track)


if __name__ == "__main__":
   gorrion = Gorrion()
   gorrion.run()
