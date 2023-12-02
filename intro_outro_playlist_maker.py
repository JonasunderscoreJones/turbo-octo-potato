'''Make a playlist of all the intro/outro songs from your followed artists'''
import os
from dotenv import load_dotenv

import top_lib

# WARNING: THIS WILL RATELIMIT THE SHIT OUT OF YOUR ACCOUNT

load_dotenv()

INTROOUTROPLAYLIST_ID = os.getenv('INTROOUTROPLAYLIST_ID')

print(INTROOUTROPLAYLIST_ID)

def track_is_eligible(track_dict:dict) -> bool:
    '''Check whether or not a track is an intro/outro

    track: track dict object from spotify api

    Returns: whether or not the track is eligble or not'''
    if track_dict['duration_ms'] < 90000:
        return True
    if "intro" in track_dict['name'].lower() or "outro" in track_dict['name'].lower():
        return True
    return False


if __name__ == "__main__":
    API_CALL_COUNT = 0
    print("Authenticating...")
    authenticator = top_lib.Auth(verbose=True)
    sp = authenticator.newSpotifyauth(
        "user-follow-read playlist-modify-public playlist-modify-private")
    spotifyManager = top_lib.SpotifyManager(sp)
    print("Authenticated!")
    print("Fetching Artists...")
    artists = spotifyManager.fetchUserFollowedArtists()
    API_CALL_COUNT += 4
    print("Found " + str(len(artists))+ " Artists!")

    track_uris = []
    ARTIST_NUM = len(artists)
    NOW_ARTIST = 0
    for artist in artists:
        NOW_ARTIST += 1
        try:
            print(f"[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] Fetching albums for", artist[1])
            albums = spotifyManager.fetchArtistAlbums(artist[0])
            API_CALL_COUNT += 1
        except top_lib.SpotifyTooManyAlbumsError:
            print(f"[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] Error fetching albums for",
                  artist[1])
            continue
        for album in albums[0]:
            print(f"[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] Fetching tracks for", album[0])
            album_track_uris = spotifyManager.getTrackUrisFromAlbum(album[1])
            API_CALL_COUNT += 1
            for track_uri in album_track_uris:
                track = sp.track(track_uri)
                API_CALL_COUNT += 1
                if track_is_eligible(track):
                    print(f"[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] " + \
                          track['artists'][0]['name'], track['name'])
                    track_uris.append(track_uri)
                    sp.playlist_add_items(INTROOUTROPLAYLIST_ID, [track_uri])
                    API_CALL_COUNT += 1
                    continue
                print(f"[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] Skipping",
                      track['artists'][0]['name'], track['name'], end="\r")
            print(f"\n[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] Done with", album[0])
        print(f"[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] Done with", artist[1])
    print(f"[{NOW_ARTIST}/{ARTIST_NUM}]{API_CALL_COUNT}] Done with all artists")
    print("TOOK THIS MANY API CALLS: ", API_CALL_COUNT)
