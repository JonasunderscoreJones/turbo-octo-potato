'''Get the last spotify track'''
import os
from dotenv import load_dotenv

import top_lib

# load .env file
load_dotenv()

# Set up your Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
PLAYLIST_ID = os.getenv('SOMEPLAYLIST_ID')

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET or \
    not SPOTIFY_REDIRECT_URI or not PLAYLIST_ID:
    raise ValueError("Please provide the required information in the .env file.")

# Create a Spotipy instance with authentication
auth_manager = top_lib.Auth(verbose=True)
sp = auth_manager.newSpotifyauth("playlist-read-private")

def get_last_track_of_playlist(playlist_id: str) -> dict:
    '''Get the last track of a playlist'''
    # Get the playlist's tracks
    playlist = sp.playlist_tracks(playlist_id)

    # Extract the last track
    return playlist["items"][-1]["track"]

# Retrieve the last track of the playlist
last_track = get_last_track_of_playlist(PLAYLIST_ID)

# Access information about the last track
print("Last Track Name:", last_track["name"])
print("Last Track Artist:", last_track["artists"][0]["name"])
print("Last Track URI:", last_track["uri"])
