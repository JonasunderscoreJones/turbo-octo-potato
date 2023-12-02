'''A script to download all the banners from the CDN and save them to a local directory.'''
import json
import os
import requests

# Define the URL pattern for downloading images
BASE_URL = "https://cdn.jonasjones.dev/project-banners"

# Define the path to the JSON file
JSON_FILE_PATH = "/home/jonas_jones/GitHub/jonasjones.dev/src/routes/projects/projects.json"

# Define the directory where you want to save the downloaded images
DOWNLOAD_DIR = os.path.expanduser("~/Downloads/uwu/")

# Create the download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

try:
    # Open and parse the JSON file
    with open(JSON_FILE_PATH, "r") as json_file:
        data = json.load(json_file)

    # Iterate through the list of objects in the JSON file
    for item in data:
        # Check if the object has a "background" property
        if "backgroud" in item:
            background_value = item["backgroud"]
            # Construct the full URL for the image
            image_url = f"{BASE_URL}{background_value}"

            # Download the image
            response = requests.get(image_url)
            if response.status_code == 200:
                # Get the filename from the URL
                filename = os.path.basename(image_url)
                # Save the image to the download directory
                with open(os.path.join(DOWNLOAD_DIR, filename), "wb") as image_file:
                    image_file.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {image_url}")
        else:
            print(f"Doesn't contain background: {item}")

except FileNotFoundError:
    print(f"JSON file not found: {JSON_FILE_PATH}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
