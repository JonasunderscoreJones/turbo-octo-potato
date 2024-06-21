import os
import requests
import json
import dotenv
import datetime

def send_webhook():
    # Load the webhook URL from the environment variables
    dotenv.load_dotenv()

    # Replace with your actual webhook URL
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    today = datetime.datetime.today().date()

    # Get the date from 7 days ago
    seven_days_ago = today - datetime.timedelta(days=7)

    # request with the date and http://api.jonasjones.dev/v1/kcomebacks/filter/daterange?start=2023-12-1&end=2023-12-16&limit=50&offset=0
    response = requests.get(f"http://api.jonasjones.dev/v1/kcomebacks/filter/daterange?start={seven_days_ago}&end={today}&limit=50&offset=0")

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        exit()

    # Parse the JSON response
    data = response.json()
    data = data['results']

    # check if there are 50 or more comebacks
    if len(data) >= 50:
        # request with offset 50
        response = requests.get(f"http://api.jonasjones.dev/v1/kcomebacks/filter/daterange?start={seven_days_ago}&end={today}&limit=50&offset=50")
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            exit()

        # Parse the JSON response
        data2 = response.json()

        # join the lists
        data += data2['results']

    # Create the message content
    content = "# Here are the comebacks from this week:\n"
    for i in data:
        content += f"{i['date']} > {i['title']} - {i['artist']}: {i['links'] if i['links'] != [] else '*No Links*'}\n"

    # Message content
    message = {
        "content": content,
    }

    # Make the POST request to the webhook URL
    response = requests.post(webhook_url, data=json.dumps(message), headers={"Content-Type": "application/json"})

    # Check if the request was successful
    if response.status_code == 204:
        print("Webhook sent successfully!")
    else:
        print(f"Failed to send webhook. Status code: {response.status_code}")


if __name__ == "__main__":
    send_webhook()