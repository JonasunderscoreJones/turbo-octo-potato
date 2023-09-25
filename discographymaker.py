import spotipy
from dotenv import load_dotenv
import top_lib

load_dotenv()

VERBOSE = True

artists = []
albums = []

def verboseprint(message: str) -> None:
    if VERBOSE:
        print(message)

def remove_duplicates(input_list: list) -> list:
    return list(set(input_list))

def getDiscographyArtist(sp: spotipy.Spotify, first = False):
    while True:
        if first:
            user_artist_input = input("Input your first Artist (name or spotify ID). Enter other's when prompted next:\n")
        else:
            print("======================")
            user_artist_input = input("Input your next Artist (name or Spotify ID). Leave empty if all have been inputed\n")
            if user_artist_input == "": return

        print("Looking up Artist...")
        try:
            if len(user_artist_input) == 22:
                if input("Did you Enter an ID? [ENTER for Yes, No for treating your Input as a name]: ") == "":
                    return user_artist_input
            search_results = sp.search(q=user_artist_input, type='artist', limit=1)
            if search_results['artists']['items'][0]['name'] != user_artist_input:
                correct_input = input(" The Artist doesn't exist on Spotify. Did you mean \"" + search_results['artists']['items'][0]['name'] + "\" [ENTER for Yes, No for retry]: ")
                if correct_input == "":
                    return search_results['artists']['items'][0]['uri'].replace("spotify:artist:", "")
                else:
                    print("All good, try again!")
                    continue
            return search_results['artists']['items'][0]['uri'].replace("spotify:artist:", "") 
        except TimeoutError:
            print("\nNetwork unreachable. Please Try again...\n")

def insertion_sort(data_list):
    for i in range(1, len(data_list)):
        current_album = data_list[i]
        current_date = current_album[2]  # Using index 2 for the release date

        j = i - 1
        while j >= 0 and data_list[j][2] > current_date:
            data_list[j + 1] = data_list[j]
            j -= 1
        data_list[j + 1] = current_album
    return data_list

def createPlaylist(sp: spotipy.Spotify, songs: list[(str, str, str, str)], userId:str, artist: str = None):
    if artist == None:
        artist = input("Primary Artist: ")
    playlist = sp.user_playlist_create(userId, artist + " Chronological Discography", description="Full Discography of " + artist + " and Solo Releases - no inst., no OSTs")
    print('New Playlist created')
    print("Name: " + playlist['name'])
    print("ID: " + playlist['id'])
    print("Description:", playlist['description'])
    print("FAILED TO SET DESCRIPTION (Spotify API Bug)\nThe playlist was created anyways") if playlist['description'] == None else None
    while len(songs) > 100:
        sp.playlist_add_items(playlist['id'], songs[:100])
        songs = songs[100:]
    sp.playlist_add_items(playlist['id'], songs)

    return playlist

if __name__ == "__main__":
    verboseprint("Authenticating...")
    authenticator = top_lib.Auth(verbose=VERBOSE)
    sp = authenticator.newSpotifyauth("playlist-modify-public playlist-modify-private")
    verboseprint("Authenticated!")

    spotifyManager = top_lib.SpotifyManager(sp)

    artist = getDiscographyArtist(sp, True)
    while artist != None:
        artists.append(artist)
        artist = getDiscographyArtist(sp)

    def sort_key(item):
        return item[2]

    verboseprint("Fetching Albums...")
    albums_unsorted = []
    for artist in remove_duplicates(artists):
        albums_unsorted.extend(spotifyManager.fetchArtistAlbums(artist)[0])
    albums = insertion_sort(albums_unsorted)
    verboseprint("Found " + str(len(albums))+ " Albums!")

    all_song_uris = []
    for album_id in albums:
        album_song_uris = spotifyManager.getTrackUrisFromAlbum(album_id[1])
        all_song_uris.extend(album_song_uris)

    playlist = createPlaylist(sp, all_song_uris, authenticator.getCreds()['SPOTIFY_USER_ID'], albums[0][3] if len(artists) == 1 else None)

    print("Playlist created! Check your Spotify!")
