import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

if 'client_id' not in os.environ.keys():
   os.environ['client_id'] = "No Key"
   os.environ['client_secret'] = "No Key"
    print('client_id and client_secret are not set, please add '
          'them in your .env file and do pipenv shell again.')

ccm = SpotifyClientCredentials(
    client_id=os.environ['client_id'],
    client_secret=os.environ['client_secret']
)
spotify = spotipy.Spotify(client_credentials_manager=ccm)
