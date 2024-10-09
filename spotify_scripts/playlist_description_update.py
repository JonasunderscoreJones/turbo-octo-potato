import spotipy
from spotipy.oauth2 import SpotifyOAuth
import hashlib
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import top_lib

def encrypt_playlist_name(name):
    # Using SHA-256 hash function, but you can choose others like MD5 or SHA-512
    hash_object = hashlib.sha256(name.encode())
    encrypted_id = hash_object.hexdigest()
    return encrypted_id

def get_playlists_with_name(sp, name):
    playlists = sp.current_user_playlists()
    matching_playlists = [playlist for playlist in playlists['items'] if name in playlist['name']]
    return matching_playlists

def main():
    # Load environment variables
    load_dotenv()

    # Set up Spotify API credentials
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

    # Set up Spotify authentication
    authenticator = top_lib.Auth(verbose=True)
    sp = authenticator.newSpotifyauth(scope="user-library-read playlist-modify-public playlist-modify-private")

    # Specify the target name in playlist
    target_name = "Chronological Discography"

    # Get playlists with the specified name
    matching_playlists = get_playlists_with_name(sp, target_name)

    counter = 0

    # Print and hash the playlist names
    for playlist in matching_playlists:
        playlist_name = playlist['name']
        encrypted_id = encrypt_playlist_name(playlist_name)

        # Print the original name and encrypted ID
        print(f"Playlist Name: {playlist_name}")
        print(f"Encrypted ID: {encrypted_id}")

        # Update the playlist description with the encrypted ID
        new_description = f"ID: {encrypted_id} - {playlist['description']}"

        print(f"New Description: {new_description}")
        # Uncomment the following line to actually update the playlist description
        sp.playlist_change_details(playlist['id'], description=new_description)

        counter += 1
        print(f"Updated {counter} playlists")

        print()

if __name__ == "__main__":
    main()
