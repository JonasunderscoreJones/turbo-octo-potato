import top_lib
import os
from dotenv import load_dotenv

# WARNING: THIS WILL RATELIMIT THE SHIT OUT OF YOUR ACCOUNT

load_dotenv()
INTROOUTROPLAYLIST_ID = os.getenv('INTROOUTROPLAYLIST_ID')

def track_is_eligible(track):
	if track['duration_ms'] < 90000:
		return True
	elif "intro" in track['name'].lower() or "outro" in track['name'].lower():
		return True
	return False



if __name__ == "__main__":
	print("Authenticating...")
	authenticator = top_lib.Auth(verbose=True)
	sp = authenticator.newSpotifyauth("user-follow-read playlist-modify-public playlist-modify-private")
	spotifyManager = top_lib.SpotifyManager(sp)
	print("Authenticated!")
	print("Fetching Artists...")
	artists = spotifyManager.fetchUserFollowedArtists()
	print("Found " + str(len(artists))+ " Artists!")

	track_uris = []

	for artist in artists:
		try:
			print("Fetching albums for", artist[1])
			albums = spotifyManager.fetchArtistAlbums(artist[0])
		except top_lib.SpotifyTooManyAlbumsError:
			print("Error fetching albums for", artist[1])
			continue
		for album in albums[0]:
			print("Fetching tracks for", album[0])
			album_track_uris = spotifyManager.getTrackUrisFromAlbum(album[1])
			for track_uri in album_track_uris:
				track = sp.track(track_uri)
				if track_is_eligible(track):
					print(track['artists'][0]['name'], track['name'])
					track_uris.append(track_uri)
					sp.playlist_add_items(INTROOUTROPLAYLIST_ID, [track_uri])
					continue
				print("Skipping", track['artists'][0]['name'], track['name'], end="\r")
			print("\nDone with", album[0])
		print("Done with", artist[1])
	print("Done with all artists")