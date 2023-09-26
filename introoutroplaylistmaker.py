import top_lib
import os
from dotenv import load_dotenv

# WARNING: THIS WILL RATELIMIT THE SHIT OUT OF YOUR ACCOUNT

load_dotenv()
INTROOUTROPLAYLIST_ID = os.getenv('INTROOUTROPLAYLIST_ID')
#INTROOUTROPLAYLIST_ID = os.getenv('RANDOMTESTPLAYLIST_ID')
print(INTROOUTROPLAYLIST_ID)

def track_is_eligible(track):
	if track['duration_ms'] < 90000:
		return True
	elif "intro" in track['name'].lower() or "outro" in track['name'].lower():
		return True
	return False


if __name__ == "__main__":
	api_call_count = 0
	print("Authenticating...")
	authenticator = top_lib.Auth(verbose=True)
	sp = authenticator.newSpotifyauth("user-follow-read playlist-modify-public playlist-modify-private")
	spotifyManager = top_lib.SpotifyManager(sp)
	print("Authenticated!")
	print("Fetching Artists...")
	artists = spotifyManager.fetchUserFollowedArtists()
	api_call_count += 4
	print("Found " + str(len(artists))+ " Artists!")

	track_uris = []
	num_artists = len(artists)
	now_artist = 0
	for artist in artists:
		now_artist += 1
		try:
			print(f"[{now_artist}/{num_artists}]{api_call_count}] Fetching albums for", artist[1])
			albums = spotifyManager.fetchArtistAlbums(artist[0])
			api_call_count += 1
		except top_lib.SpotifyTooManyAlbumsError:
			print(f"[{now_artist}/{num_artists}]{api_call_count}] Error fetching albums for", artist[1])
			continue
		for album in albums[0]:
			print(f"[{now_artist}/{num_artists}]{api_call_count}] Fetching tracks for", album[0])
			album_track_uris = spotifyManager.getTrackUrisFromAlbum(album[1])
			api_call_count += 1
			for track_uri in album_track_uris:
				track = sp.track(track_uri)
				api_call_count += 1
				if track_is_eligible(track):
					print(f"[{now_artist}/{num_artists}]{api_call_count}] " + track['artists'][0]['name'], track['name'])
					track_uris.append(track_uri)
					sp.playlist_add_items(INTROOUTROPLAYLIST_ID, [track_uri])
					api_call_count += 1
					continue
				print(f"[{now_artist}/{num_artists}]{api_call_count}] Skipping", track['artists'][0]['name'], track['name'], end="\r")
			print(f"\n[{now_artist}/{num_artists}]{api_call_count}] Done with", album[0])
		print(f"[{now_artist}/{num_artists}]{api_call_count}] Done with", artist[1])
	print(f"[{now_artist}/{num_artists}]{api_call_count}] Done with all artists")
	print("TOOK THIS MANY API CALLS: ", api_call_count)