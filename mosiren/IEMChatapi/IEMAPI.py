import requests
import os
import json
import time

# Directory where the JSON file will be saved
OUTPUT_DIR = "/app/api/"  # Glitch uses /app as the root directory
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "IEMChat_SGF.json")

def fetch_and_save_chat_feed():
    room_name = "sgfchat"  # Replace with the default room name
    seqnum = 1
    url = "https://weather.im/iembot-json/room/{0}?seqnum={1}".format(room_name, seqnum)

    headers = {
        'User-Agent': 'YourCustomUserAgent'  # Add your custom User-Agent here
    }

    try:
        # Fetch data from the external API
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Write the data to a file
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)  # Create the directory if it doesn't exist
        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Chat feed updated successfully: {OUTPUT_FILE}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching chat feed: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_save_chat_feed()
        time.sleep(3)  # Fetch new data every 5 seconds
