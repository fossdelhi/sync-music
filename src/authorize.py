import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


ccm = SpotifyClientCredentials(
          client_id = os.environ['client_id'],
          client_secret = os.environ['client_secret']
          )
spotify = spotipy.Spotify(client_credentials_manager=ccm)
