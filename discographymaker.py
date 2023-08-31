SPOTIFY_KEY = ""
SPOTIFY_SECRET = ""
SPOTIFY_USER_ID = ""

VERBOSE = True

import spotipy
from spotipy.oauth2 import SpotifyOAuth

artists = []
albums = []

def verboseprint(message: str) -> None:
    if VERBOSE:
        print(message)

def remove_duplicates(input_list: list) -> list:
    return list(set(input_list))

def spotifyauth() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_KEY,
                                        client_secret=SPOTIFY_SECRET,
                                        redirect_uri="http://localhost:6969",
                                        scope="playlist-modify-public playlist-modify-private"))

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

def ArtistAlbumGarbageHandler(apiresponse: list):
    this_artist_album_part = []
    for i in apiresponse['items']:
        this_artist_album_part.append((i['name'], i['id'], i['release_date'], i['artists'][0]['name']))
    verboseprint("Found " + str(len(this_artist_album_part)) + " Albums for " + apiresponse['items'][0]['artists'][0]['name'])
    return this_artist_album_part


def getArtistAlbum(sp: spotipy.Spotify, artists: list[str]) -> list[(str, str, str, str)]:
    albums = []
    for artist in artists:
        try:
            this_artist_albums = []
            this_artist_album_part_garbage = sp.artist_albums(artist_id=artist, album_type="album,single,compilation", limit=50)
            this_artist_albums = ArtistAlbumGarbageHandler(this_artist_album_part_garbage)
            if this_artist_album_part_garbage['total'] > 50:
                print("There currently is a bug in the Spotify API that prevents fetching anything after the first 50 Albums. Given that your artist " + this_artist_album_part_garbage['items'][0]['artists'][0]['name'] + " has more than 50 Albums, you'll need to manually add the missing ones.")
                if input("Alternatively, you can end the script here since albums will be out of order [(E/e) to end] ") in ["E", "e", "end", "End"]:
                    exit()

            albums.append(this_artist_albums)
                
        except TimeoutError:
            print("\nNetwork unreachable. THIS IS NOT RECOVERABLE. Please restart the process")
            exit()
    return albums

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

def createPlaylist(sp: spotipy.Spotify, songs: list[(str, str, str, str)], artist: str = None):
    if artist == None:
        artist = input("Primary Artist: ")
    playlist = sp.user_playlist_create(SPOTIFY_USER_ID, artist + " Chronological Discography", description="Full Discography of " + artist + "and Solo Releases - no inst., no OSTs")
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

def get_song_uris(album_id):
    album_tracks = sp.album_tracks(album_id)
    song_uris = [track['uri'] for track in album_tracks['items']]
    return song_uris

verboseprint("Authenticating...")
sp = spotifyauth()
verboseprint("Authenticated!")

artist = getDiscographyArtist(sp, True)
while artist != None:
    artists.append(artist)
    artist = getDiscographyArtist(sp)

def sort_key(item):
    return item[2]

verboseprint("Fetching Albums...")
albums_unsorted = [item for sublist in getArtistAlbum(sp, remove_duplicates(artists)) for item in sublist]
albums = insertion_sort(albums_unsorted)
verboseprint("Found " + str(len(albums))+ " Albums!")

all_song_uris = []
for album_id in albums:
    album_song_uris = get_song_uris(album_id[1])
    all_song_uris.extend(album_song_uris)

playlist = createPlaylist(sp, all_song_uris, albums[0][3] if len(artists) == 1 else None)

print("Playlist created! Check your Spotify!")
