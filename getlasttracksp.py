import spotipy, os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Set up your Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
PLAYLIST_ID = os.getenv('SOMEPLAYLIST_ID')

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET or not SPOTIFY_REDIRECT_URI or not PLAYLIST_ID:
		raise ValueError("Please provide the required information in the .env file.")

# Create a Spotipy instance with authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope="playlist-read-private"))

def get_last_track_of_playlist(playlist_id):
    # Get the playlist's tracks
    playlist = sp.playlist_tracks(playlist_id)

    # Extract the last track
    last_track = playlist["items"][-1]["track"]

    return last_track

# Replace "YOUR_PLAYLIST_ID" with the actual playlist ID
playlist_id = PLAYLIST_ID
last_track = get_last_track_of_playlist(playlist_id)

# Access information about the last track
print("Last Track Name:", last_track["name"])
print("Last Track Artist:", last_track["artists"][0]["name"])
print("Last Track URI:", last_track["uri"])
