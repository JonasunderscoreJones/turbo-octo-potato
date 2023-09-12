import pylast, spotipy, sys, os, time
from spotipy.oauth2 import SpotifyOAuth

# Define your Last.fm API credentials
LASTFM_API_KEY = ""
LASTFM_API_SECRET = ""
LASTFM_USERNAME = "Jonas_Jones"
LASTFM_PASSWORD_HASH = pylast.md5("")

# Define your Spotify API credentials
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""

# Define your playlist IDs
LIKEDSONGPLAYLIST_ID = ""

def progress_bar(current, total, last_time_stamp=time.time()):
    this_timestamp = time.time()
    width = os.get_terminal_size().columns
    progress = round((current/total)*width)
    total_num_len = len(str(total))
    if width < 2* total_num_len + 15:
        return f"{current}/{total}", this_timestamp
    else:
        current_spacer = " "*(total_num_len-len(str(current)))
        eta = round((total - current)* (this_timestamp - last_time_stamp)/60)
        percent = str(round(current/total*100))
        percent = " "*(3-len(percent)) + percent
        progress_bar_length = width - 2*total_num_len - 14 - len(str(eta)) - len(percent)
        progress_bar_progress = round((current/total)*progress_bar_length)
        progress_bar_spacer = " "*(progress_bar_length-progress_bar_progress)
        return f"[{current_spacer}{current}/{total}|{percent}%|ETA: {eta}s|{'='*progress_bar_progress}>{progress_bar_spacer}]", this_timestamp

def verboseprint(message, end="\n"):
    if VERBOSE_LOGGING:
        print(message, end=end)

def handle_playlist_part_return(playlist_part, all_songs):
    for item in playlist_part["items"]:
        track_uri = item["track"]["uri"]
        track_name = item["track"]["name"]
        artist_name = item["track"]["artists"][0]["name"]
        all_songs.append((track_uri, track_name, artist_name))
        
    return all_songs

def get_all_songs_from_playlist(playlist_id):
    verboseprint("Fetching songs from the liked songs playlist...")
    all_songs = []
    limit = 100  # Adjust the limit based on your needs
    offset = 0
    last_time_stamp = time.time()

    while True:
        playlist_part = sp.playlist_items(playlist_id, limit=limit, offset=offset)
        if not playlist_part["items"]:
            break
        all_songs = handle_playlist_part_return(playlist_part, all_songs)
        
        progress_print, last_time_stamp = progress_bar(offset+limit, playlist_part["total"], last_time_stamp)
        verboseprint(progress_print, end="\r")

        offset += limit
    verboseprint("")
    return all_songs

def get_all_liked_songs():
    verboseprint("Fetching liked songs...")
    verboseprint("This may take a while... (the API only allows for 50 songs per request for the liked songs)")
    all_liked_songs = []
    limit = 50  # Adjust the limit based on your needs
    offset = 0
    last_time_stamp = time.time()

    while True:
        liked_songs_chunk = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not liked_songs_chunk["items"]:
            break
        all_liked_songs = handle_playlist_part_return(liked_songs_chunk, all_liked_songs)
        
        progress_print, last_time_stamp = progress_bar(offset+limit, liked_songs_chunk["total"], last_time_stamp)
        verboseprint(progress_print, end="\r")

        offset += limit
    verboseprint("")
    return all_liked_songs

def is_track_in_playlist(playlist_song_list, track_uri):
    playlist_tracks = playlist_song_list
    for item in playlist_tracks:
        if item[0] == track_uri:
            return True
    return False

def add_track_to_playlist(playlist_id, track_uri):
    sp.playlist_add_items(playlist_id, [track_uri])

def remove_unliked_tracks(primary_playlist_id, liked_tracks):
    verboseprint("Removing unliked tracks from the primary playlist...")
    liked_track_uris = [track_uri for track_uri, _, _ in liked_tracks]
    primary_playlist_tracks = get_all_songs_from_playlist(primary_playlist_id)
    
    #tracks_to_remove = [track_uri for track_uri in primary_playlist_tracks if track_uri not in liked_track_uris]

    tracks_to_remove = []
    for track_uri, _, _ in primary_playlist_tracks:
        if track_uri not in liked_track_uris:
            tracks_to_remove.append(track_uri)
    
    if tracks_to_remove:
        sp.playlist_remove_all_occurrences_of_items(primary_playlist_id, tracks_to_remove)
        print(f"Removed {len(tracks_to_remove)} unliked track(s) from the primary playlist.")
        print(f"Track URIs: {tracks_to_remove}")

if __name__ == "__main__":

    # Parse command-line arguments
    VERBOSE_LOGGING = "-v" in sys.argv or "--verbose" in sys.argv
    try:
        SKIPSONGS = int(sys.argv[sys.argv.index("--skip") + 1]) if "--skip" in sys.argv else int(sys.argv[sys.argv.index("-s") + 1]) if "-s" in sys.argv else 0
    except:
        print("[--skip/-s] Require a number to be set.")
        print("E.g.: --skip 88")
        exit()


    verboseprint("Authenticating Spotify...")

    # Create a Spotipy instance with authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope="user-library-read playlist-modify-public playlist-modify-private"))

    verboseprint("Authenticating Last.fm...")

    # Set up Last.fm network
    network = pylast.LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET, username=LASTFM_USERNAME, password_hash=LASTFM_PASSWORD_HASH)

    # Main loop for syncing liked songs
    liked_songs = get_all_liked_songs()

    #remove_unliked_tracks(LIKEDSONGPLAYLIST_ID, liked_songs)

    liked_songs_playlist_songs = get_all_songs_from_playlist(LIKEDSONGPLAYLIST_ID)

    print(f"Number of liked tracks: {len(liked_songs)}")
    print(f"Number of playlist songs: {len(liked_songs_playlist_songs)}")
    print(f"Skipping the first {SKIPSONGS} songs...")
    tracknr = 0
    for track_uri, track_name, artist_name in liked_songs:
        tracknr += 1
        # Love the track on Last.fm
        def loop_do():
            track = sp.track(track_uri)
            fm_track = network.get_track(artist_name, track_name)
            fm_track.love()
            fm_track.add_tags(("awesome", "favorite"))
            
            if not is_track_in_playlist(liked_songs_playlist_songs, track_uri):
                add_track_to_playlist(LIKEDSONGPLAYLIST_ID, track_uri)
                if VERBOSE_LOGGING:
                    verboseprint("%-10s %15s" % (f"ETA:{round((((int(len(liked_songs))-tracknr)*0.75)/60))}min", f"[{tracknr}/{int(len(liked_songs))}|+]") + "%30.32s %s" % (track['artists'][0]['name'], track['name']))
            elif VERBOSE_LOGGING:
                verboseprint("%-10s %13s" % (f"ETA:{round((((int(len(liked_songs))-tracknr)*0.75)/60))}min", f"[{tracknr}/{int(len(liked_songs))}]") + "%32.32s %s" % (track['artists'][0]['name'], track['name']))
        # Loop until the API call succeeds
        while tracknr > SKIPSONGS:
            try:
                loop_do()
                break
            except KeyboardInterrupt: # Allow the user to interrupt the script
                exit()
            except:
                continue
