import pylast, time

# Replace with your Last.fm API credentials
API_KEY = ""
API_SECRET = ""
USERNAME = "Jonas_Jones"
PASSWORD = ""  # Leave this empty if you're not using a password

# Create a Last.fm network object
network = pylast.LastFMNetwork(
    api_key=API_KEY, api_secret=API_SECRET, username=USERNAME, password_hash=PASSWORD
)

def get_listened_artists():
    user = network.get_user(USERNAME)
    recent_tracks = user.get_recent_tracks(limit=None)  # Fetch all recent tracks
    listened_artists = set()
    for track in recent_tracks:
        artist = track.track.artist
        if not artist in listened_artists:
            print(artist)
            listened_artists.add(artist)

    return listened_artists

if __name__ == "__main__":
    start = time.time()
    listened_artists = get_listened_artists()
    end = time.time()
    print("Listened Artists:")
    for artist in listened_artists:
        print(artist)
    
    print("Time elapsed: " + str(end - start) + " seconds")
