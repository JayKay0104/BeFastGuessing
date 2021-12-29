import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


def return_client(scope: str = "user-library-read,streaming,app-remote-control") -> spotipy.Spotify:
    """ returns the spotify client from spotipy """
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
                                                     client_secret=os.environ.get(
                                                         "SPOTIFY_CLIENT_SECRET"),
                                                     redirect_uri=os.environ.get(
                                                         "SPOTIFY_REDIRECT"),
                                                     scope=scope))
