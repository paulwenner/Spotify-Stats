import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'd7674a5f7c6c4621be709958d79fe2c4'
client_secret = 'a78354b8411e44ac91f2183709f48569'

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

results = sp.search(q='artist:Beatles', type='track')
print(results)

