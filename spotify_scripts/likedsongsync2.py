'''A script to sync your liked songs from Spotify to Last.fm and a Spotify 
playlist that can be made public (unlike the built-in liked songs playlist).'''
import time
from dotenv import load_dotenv
import spotipy
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import top_lib



def progress_bar(current, total, last_time_stamp=float, etastr=None):
    '''A function to print a progress bar to the terminal.
    current: The current progress
    total: The total progress
    last_time_stamp: The time stamp of the last call of this function
    etastr: The estimated time until completion as a string
    
    Returns: A string with the progress bar'''
    current = total if current > total else current
    this_timestamp = time.time()
    width = os.get_terminal_size().columns
    #progress = round((current/total)*width)
    total_num_len = len(str(total))
    if width < 2* total_num_len + 15:
        return f"{current}/{total}", this_timestamp

    current_spacer = " "*(total_num_len-len(str(current)))
    if etastr:
        eta = etastr
    else:
        eta = str(round((total - current) *
                        (this_timestamp - last_time_stamp)/60)) + "s"
    percent = str(round(current/total*100))
    percent = " "*(3-len(percent)) + percent
    progress_bar_length = width - 2 * \
        total_num_len - 13 - len(str(eta)) - len(percent)
    progress_bar_progress = round((current/total)*progress_bar_length)
    progress_bar_spacer = " "*(progress_bar_length-progress_bar_progress)
    return f"[{current_spacer}{current}/{total}|{percent}%|ETA: {eta}|" + \
        f"{'='*progress_bar_progress}>{progress_bar_spacer}]", \
        this_timestamp

def verboseprint(message, end="\n"):
    '''A function to print verbose output.
    
    message: The message to print
    end: The end character to use for the print function'''
    if VERBOSE_LOGGING:
        print(message, end=end)

def handle_playlist_part_return(playlist_part:str, all_songs:list):
    '''A function to handle parsing the playlist part and adding them to the 
    list of all songs.

    playlist_part: The playlist part to handle
    all_songs: The list of all songs to append the new songs to

    Returns: The updated list of all songs'''
    for item in playlist_part["items"]:
        track_uri = item["track"]["uri"]
        track_name = item["track"]["name"]
        artist_name = item["track"]["artists"][0]["name"]
        all_songs.append((track_uri, track_name, artist_name))

    return all_songs

def get_all_songs_from_playlist(playlist_id):
    '''A function to get all songs from a playlist.
    
    playlist_id: The ID of the playlist to get the songs from
    
    Returns: A list of all songs in the playlist'''
    verboseprint("Fetching songs from the liked songs playlist...")
    progressbar = top_lib.Progressbar()
    progress_bar_eta_manager = top_lib.ProgressBarEtaManager()
    all_songs = []
    limit = 100
    offset = 0

    while True:
        playlist_part = sp.playlist_items(playlist_id,
                                          limit=limit,
                                          offset=offset)
        if not playlist_part["items"]:
            break
        all_songs = handle_playlist_part_return(playlist_part, all_songs)

        progress_bar_eta_manager.now()
        progressbar.setTotal(playlist_part["total"])
        progress_print = progressbar.buildSnapshot(offset+limit,
                                                   progress_bar_eta_manager
                                                        .getAvgEta()/limit)
        verboseprint(progress_print, end="\r")

        offset += limit
    verboseprint("")
    return all_songs

def get_all_liked_songs():
    '''A function to get all liked songs from Spotify.

    Returns: A list of all liked songs'''
    verboseprint("Fetching liked songs...")
    verboseprint("This may take a while...(the API only allows for " + \
                 "50 songs per request for the liked songs)")
    progressbar = top_lib.Progressbar()
    progress_bar_eta_manager = top_lib.ProgressBarEtaManager()
    all_liked_songs = []
    limit = 50
    offset = 0

    while True:
        liked_songs_chunk = sp.current_user_saved_tracks(limit=limit,
                                                         offset=offset)
        if not liked_songs_chunk["items"]:
            break
        all_liked_songs = handle_playlist_part_return(liked_songs_chunk,
                                                      all_liked_songs)

        progress_bar_eta_manager.now()
        progressbar.setTotal(liked_songs_chunk["total"])
        progress_print = progressbar.buildSnapshot(offset+limit,
                                                   progress_bar_eta_manager
                                                        .getAvgEta()/limit)
        verboseprint(progress_print, end="\r")

        offset += limit
    verboseprint("")
    return all_liked_songs

def is_track_in_playlist(playlist_song_list, track_uri):
    '''A function to check if a track is in a playlist.

    playlist_song_list: The list of songs in the playlist
    track_uri: The URI of the track to check

    Returns: True if the track is in the playlist, False otherwise'''
    playlist_tracks = playlist_song_list
    for item in playlist_tracks:
        if item[0] == track_uri:
            return True
    return False

def add_track_to_playlist(playlist_id, track_uri):
    '''A function to add a track to a playlist.

    playlist_id: The ID of the playlist to add the track to
    track_uri: The URI of the track to add to the playlist'''
    sp.playlist_add_items(playlist_id, [track_uri])

def main():
    # load .env file
    load_dotenv()

    # because im lazy
    global VERBOSE_LOGGING
    global sp

    # Define your playlist IDs
    LIKEDSONGPLAYLIST_ID = os.getenv('LIKEDSONGPLAYLIST_ID')

    # Parse command-line arguments
    VERBOSE_LOGGING = "-v" in sys.argv or "--verbose" in sys.argv
    FORCE_RESYNC_ALL = "-f" in sys.argv or "--force-all" in sys.argv

    try:
        SKIPSONGS = int(sys.argv[sys.argv.index("--skip") + 1]) if "--skip" \
            in sys.argv else int(sys.argv[sys.argv.index("-s") + 1]) \
                if "-s" in sys.argv else 0
    except ValueError:
        print("[--skip/-s] Require a number to be set.")
        print("E.g.: --skip 88")
        sys.exit(-1)

    verboseprint("Authenticating Spotify...")

    authenticator = top_lib.Auth(verbose=VERBOSE_LOGGING)

    # Create a Spotipy instance with authentication
    sp = authenticator.newSpotifyauth(
        scope="user-library-read playlist-modify-public playlist-modify-private")

    verboseprint("Authenticating Last.fm...")

    # Set up Last.fm network
    network = authenticator.newLastfmauth()

    # Main loop for syncing liked songs
    liked_songs = get_all_liked_songs()

    liked_songs_playlist_songs = get_all_songs_from_playlist(LIKEDSONGPLAYLIST_ID)

    if not FORCE_RESYNC_ALL:
        verboseprint("Syncing only new songs...")
        liked_songs = [x for x in liked_songs if x not in liked_songs_playlist_songs]
        if len(liked_songs) == 0:
            print("Nothing to do.")
            sys.exit(0)
    verboseprint(f"Number of playlist songs: {len(liked_songs_playlist_songs)}")
    verboseprint(f"Skipping the first {SKIPSONGS} songs...")
    TRACK_NR = 0
    last_time_stamp = time.time()
    progressbar = top_lib.Progressbar()
    progressbar.setTotal(len(liked_songs))
    progressBarEtaManager = top_lib.ProgressBarEtaManager()
    for track_uri, track_name, artist_name in liked_songs[::-1]:
        TRACK_NR += 1

        def loop_do(last_time_stamp):
            '''A function to loop until the API call succeeds.

            last_time_stamp: The time stamp of the last call of this function

            Returns: The time stamp of the last call of this function'''
            track = sp.track(track_uri)
            fm_track = network.get_track(artist_name, track_name)
            fm_track.love()
            fm_track.add_tags(("awesome", "favorite"))
            verboseprint(' '* os.get_terminal_size().columns, end="\r")
            if not is_track_in_playlist(liked_songs_playlist_songs, track_uri):
                verboseprint("[" + f"%{4 + len(str(len(liked_songs)))*2}s" %
                             (f"{TRACK_NR}/{len(liked_songs)}|+]") +
                             "%30.32s %s" % (track['artists'][0]['name'],
                                             track['name']))

            else:
                verboseprint("[" + f"%{2 + len(str(len(liked_songs)))*2}s" %
                             (f"{TRACK_NR}/{len(liked_songs)}]") +
                             "%32.32s %s" % (track['artists'][0]['name'],
                                             track['name']))

            progressBarEtaManager.now()
            #print(progressBarEtaManager.getDurations())
            #print(tracknr)
            progress_print = progressbar.buildSnapshot(TRACK_NR,
                                                       progressBarEtaManager
                                                            .getAvgEta())
            #print(progressBarEtaManager.getDurations())
            verboseprint(progress_print, end="\r")
            if not is_track_in_playlist(liked_songs_playlist_songs, track_uri):
                add_track_to_playlist(LIKEDSONGPLAYLIST_ID, track_uri)

            return last_time_stamp
        # Loop until the API call succeeds
        while TRACK_NR > SKIPSONGS:
            try:
                last_time_stamp =  loop_do(last_time_stamp)
                break
            except KeyboardInterrupt: # Allow the user to interrupt the script
                print("Interrupted by user.")
                sys.exit(0)
            except spotipy.SpotifyException as e:
                if e.http_status == 429:
                    time.sleep(30)
                    verboseprint("                       ]")
                    verboseprint("WARN:RATELIMIT EXCEEDED] Waiting 30 seconds to proceed...")
                else:
                    verboseprint(e.http_status)
            except Exception:
            #except e:
                continue


if __name__ == "__main__":
    main()
