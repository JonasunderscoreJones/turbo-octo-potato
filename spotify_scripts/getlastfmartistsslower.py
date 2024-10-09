import pylast

# Replace with your Last.fm API credentials
API_KEY = ""
API_SECRET = ""
USERNAME = "Jonas_Jones"
PASSWORD = ""  # Leave this empty if you're not using a password

# Create a Last.fm network object
network = pylast.LastFMNetwork(
    api_key=API_KEY, api_secret=API_SECRET, username=USERNAME, password_hash=PASSWORD
)

def get_listened_artists(limit_per_batch=100):
    user = network.get_user(USERNAME)
    
    page = 1
    listened_artists = set()

    while True:
        recent_tracks = user.get_recent_tracks(limit=limit_per_batch, page=page)
        if not recent_tracks:
            break

        for track in recent_tracks:
            artist = track.track.artist
            listened_artists.add(artist)

        page += 1

    return listened_artists

if __name__ == "__main__":
    listened_artists = get_listened_artists()
    
    print("Listened Artists:")
    for artist in listened_artists:
        print(artist)
 
