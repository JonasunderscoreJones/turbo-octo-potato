import os, spotipy, pylast
from spotipy.oauth2 import SpotifyOAuth
from typing import Union
from dotenv import load_dotenv

load_dotenv()

class SpotifyTooManyAlbumsError(Exception):
    """Raised when an artist has more than 50 albums since the spotify API currently has a bug that prevents fetching more than the last 50 albums"""
    pass

class Auth:
    """Authentication for Spotify and Last.fm"""
    def __init__(self, verbose:bool=True, lastfm_network:pylast.LastFMNetwork=None, spotify:spotipy.Spotify=None) -> None:
        load_dotenv()
        self.LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
        self.LASTFM_API_SECRET = os.getenv('LASTFM_API_SECRET')
        self.LASTFM_USERNAME = os.getenv('LASTFM_USERNAME')
        self.LASTFM_PASSWORD_HASH = os.getenv('LASTFM_PASSWORD_HASH')
        self.SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        self.SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.SPOTIPY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
        self.SPOTIFY_USER_ID = os.getenv('SPOTIFY_USER_ID')
        self.VERBOSE = verbose
        self.lastfm_network = lastfm_network
        self.spotify = spotify

    def verbose(self, verbose:bool=False) -> None:
        """Set verbose mode"""
        self.VERBOSE = verbose

    def newLastfmauth(self) -> pylast.LastFMNetwork:
        """
        Authenticate with Last.fm

        Returns:
            pylast.LastFMNetwork: Last.fm network object
        """

        if not self.LASTFM_API_KEY or not self.LASTFM_API_SECRET or not self.LASTFM_USERNAME or not self.LASTFM_PASSWORD_HASH:
            raise ValueError("Please provide LASTFM_API_KEY, LASTFM_API_SECRET, LASTFM_USERNAME, and LASTFM_PASSWORD_HASH in the .env file.")

        SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".lfm_session_key")
        self.lastfm_network = pylast.LastFMNetwork(self.LASTFM_API_KEY, self.LASTFM_API_SECRET)
        if not os.path.exists(SESSION_KEY_FILE):
            skg = pylast.SessionKeyGenerator(self.lastfm_network)
            url = skg.get_web_auth_url()

            print(f"Please authorize this script to access your account: {url}\n")
            import time
            import webbrowser

            webbrowser.open(url)

            while True:
                try:
                    session_key = skg.get_web_auth_session_key(url)
                    with open(SESSION_KEY_FILE, "w") as f:
                        f.write(session_key)
                    break
                except pylast.WSError:
                    time.sleep(1)
        else:
            session_key = open(SESSION_KEY_FILE).read()

        self.lastfm_network.session_key = session_key
        return self.lastfm_network

    def newSpotifyauth(self, scope:str) -> spotipy.Spotify:
        """
        Authenticate with Spotify

        Returns:
            spotipy.Spotify: Spotify object
        """

        if not self.SPOTIPY_CLIENT_ID or not self.SPOTIPY_CLIENT_SECRET or not self.SPOTIPY_REDIRECT_URI:
            raise ValueError("Please provide SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI in the .env file.")

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                            client_secret=self.SPOTIPY_CLIENT_SECRET,
                                            redirect_uri=self.SPOTIPY_REDIRECT_URI,
                                            scope=scope))
        return self.spotify

    def getSpotify(self) -> spotipy.Spotify:
        """Get Spotify object"""
        return self.spotify

    def getLastfm(self) -> pylast.LastFMNetwork:
        """Get Last.fm network object"""
        return self.lastfm_network

    def getCreds(self) -> dict:
        """
        Get credentials

        Returns:
            dict: Dictionary with credentials
        """

        return {
            "LASTFM_API_KEY": self.LASTFM_API_KEY,
            "LASTFM_API_SECRET": self.LASTFM_API_SECRET,
            "LASTFM_USERNAME": self.LASTFM_USERNAME,
            "LASTFM_PASSWORD_HASH": self.LASTFM_PASSWORD_HASH,
            "SPOTIPY_CLIENT_ID": self.SPOTIPY_CLIENT_ID,
            "SPOTIPY_CLIENT_SECRET": self.SPOTIPY_CLIENT_SECRET,
            "SPOTIPY_REDIRECT_URI": self.SPOTIPY_REDIRECT_URI,
            "SPOTIFY_USER_ID": self.SPOTIFY_USER_ID,
        }

class SpotifyManager:
    def __init__(self, spotify:spotipy.Spotify) -> None:
        self.spotify = spotify

    def _artistAlbumGarbageHandler(self, apiresponse: str):
        this_artist_album_part = []
        for i in apiresponse['items']:
            this_artist_album_part.append((i['name'], i['id'], i['release_date'], i['artists'][0]['name']))
        #verboseprint("Found " + str(len(this_artist_album_part)) + " Albums for " + apiresponse['items'][0]['artists'][0]['name'])
        return this_artist_album_part

    def fetchArtistAlbums(self, artist: str) -> list[(str, str, str, str)]:
        albums = []
        try:
            this_artist_albums = []
            this_artist_album_part_garbage = self.spotify.artist_albums(artist_id=artist, album_type="album,single,compilation", limit=50)
            this_artist_albums = self._artistAlbumGarbageHandler(this_artist_album_part_garbage)
            if this_artist_album_part_garbage['total'] > 50:
                print("There currently is a bug in the Spotify API that prevents fetching anything after the first 50 Albums. Given that your artist " + this_artist_album_part_garbage['items'][0]['artists'][0]['name'] + " has more than 50 Albums, you'll need to manually add the missing ones.")
                if input("Alternatively, you can end the script here since albums will be out of order [(E/e) to end] ") in ["E", "e", "end", "End"]:
                    exit()

            albums.append(this_artist_albums)

        except TimeoutError:
            print("\nNetwork unreachable. THIS IS NOT RECOVERABLE. Please restart the process")
            exit()
        return albums

    def getTrackUrisFromAlbum(self, album_id: str) -> list[str]:
        album_tracks = self.spotify.album_tracks(album_id)
        song_uris = [track['uri'] for track in album_tracks['items']]
        return song_uris