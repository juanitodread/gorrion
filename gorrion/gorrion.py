from config import Config
from clients.spotify.client import Spotify


class Gorrion:
    def run(self):
        spotify = Spotify(Config.SPOTIFY_CLIENT_TOKEN)
        current_track = spotify.get_current_track()
        print('CURRENT_TRACK: ', current_track)


if __name__ == "__main__":
    gorrion = Gorrion()
    gorrion.run()
