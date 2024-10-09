import requests
from datetime import datetime
import json
import urllib.parse
import time
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

starttime = time.time()

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
LASTFM_USERNAME = os.getenv('LASTFM_USERNAME')

if not LASTFM_API_KEY or not LASTFM_USERNAME:
    raise ValueError("Please provide the required information in the .env file.")

# Get the total number of scrobbles for the user
url = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json"
response = requests.get(url)
data = response.json()
total_scrobbles = int(data['user']['playcount'])

# Calculate the number of pages required for pagination
page_count = (total_scrobbles + 200 - 1) // 200

# Fetch all scrobbles by paginating through the API responses
all_scrobbles = []
for page in range(1, page_count + 1):
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&page={page}"
    response = requests.get(url)
    data = response.json()
    tracks = data['recenttracks']['track']

    for track in tracks:
        artist = urllib.parse.quote(track['artist']['#text'])
        song = urllib.parse.quote(track['name'])

        track_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={LASTFM_API_KEY}&artist={artist}&track={song}&format=json"
        #print(track_url)
        track_response = requests.get(track_url)
        track_data = track_response.json()
        duration = int(track_data['track']['duration'])
        track['duration'] = duration
        all_scrobbles.append(track)

# Save the song list to a JSON file
output_file = "song_list.json"
with open(output_file, "w") as file:
    json.dump(all_scrobbles, file)

total_duration = sum(track['duration'] for track in all_scrobbles)

print(total_duration)
# Convert the total listening time to a human-readable format
total_time = datetime.utcfromtimestamp(total_duration).strftime('%H:%M:%S')

print(f"Overall Listening Time: {total_time}")

print(f"Took: {time.time() - starttime}")