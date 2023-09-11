import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up your Spotify API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "YOUR_REDIRECT_URI"

# Create a Spotipy instance with authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="playlist-read-private"))

def get_last_track_of_playlist(playlist_id):
    # Get the playlist's tracks
    playlist = sp.playlist_tracks(playlist_id)
    
    # Extract the last track
    last_track = playlist["items"][-1]["track"]
    
    return last_track

# Replace "YOUR_PLAYLIST_ID" with the actual playlist ID
playlist_id = "YOUR_PLAYLIST_ID"
last_track = get_last_track_of_playlist(playlist_id)

# Access information about the last track
print("Last Track Name:", last_track["name"])
print("Last Track Artist:", last_track["artists"][0]["name"])
print("Last Track URI:", last_track["uri"])
