import requests
import time
from threading import Thread
import json
import os

# Constants
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN'] # telegram bot token
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID'] # telegram chat id
AUTHORIZED_USER_ID = os.environ['AUTHORIZED_USER_ID'] # telegram authorized user id
CHECK_INTERVAL = os.environ['CHECK_INTERVAL']  # check interval in seconds
DATA_FILE = os.environ['DATA_FILE'] # whete is store datafile

# Load Docker images from a file
def load_docker_images():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save Docker images to a file
def save_docker_images(docker_images):
    with open(DATA_FILE, 'w') as file:
        json.dump(docker_images, file)

docker_images = load_docker_images()

def get_latest_docker_tags(image):
    # Automatically prefix "library/" if the image does not contain any "/"
    if '/' not in image:
        image = f"library/{image}"
    url = f"https://registry.hub.docker.com/v2/repositories/{image}/tags"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        if 'results' in data:
            tags = [tag['name'] for tag in data['results']]
            return tags
        else:
            raise ValueError("No 'results' key in response")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")  # Handle specific HTTP errors
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")  # Handle connection errors
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")  # Handle timeouts
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else, {err}")  # Handle any other error
    except ValueError as ve:
        print(ve)  # Handle missing 'results' key in JSON
    return []  # Return an empty list if there's an error

def send_telegram_message(message, chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
    requests.post(url, data=data)

def monitor_docker_images():
    interval = int(CHECK_INTERVAL)  # Convert the string interval to an integer for the sleep function
    while True:
        time.sleep(interval)
        for image in list(docker_images.keys()):
            current_tags = get_latest_docker_tags(image)
            new_tags = [tag for tag in current_tags if tag not in docker_images[image]]
            if new_tags:
                for tag in new_tags:
                    message = f"New Docker image tag for [{image}](https://hub.docker.com/r/{image}/tags?name={tag}): `{tag}`"
                    send_telegram_message(message, TELEGRAM_CHAT_ID)
                docker_images[image] = current_tags
        save_docker_images(docker_images)

def handle_updates():
    last_update_id = 0
    while True:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_update_id+1}&timeout=10"
        response = requests.get(url).json()
        for update in response.get('result', []):
            last_update_id = update['update_id']
            if 'message' in update and 'text' in update['message']:
                user_id = str(update['message']['from']['id'])  # Convert the incoming user ID to string for comparison
                message_text = update['message']['text']
                chat_id = update['message']['chat']['id']

                if user_id != AUTHORIZED_USER_ID:
                    send_telegram_message("You are not authorized to control this bot.", chat_id)
                    continue

                if message_text.startswith('/add '):
                    new_image = message_text.split('/add ', 1)[1].strip()
                    if new_image not in docker_images:
                        docker_images[new_image] = get_latest_docker_tags(new_image)
                        send_telegram_message(f"Added new Docker image for monitoring: {new_image}", chat_id)
                        save_docker_images(docker_images)
                    else:
                        send_telegram_message("This Docker image is already being monitored.", chat_id)
                elif message_text.startswith('/remove '):
                    image_to_remove = message_text.split('/remove ', 1)[1].strip()
                    if image_to_remove in docker_images:
                        del docker_images[image_to_remove]
                        send_telegram_message(f"Removed Docker image from monitoring: {image_to_remove}", chat_id)
                        save_docker_images(docker_images)
                    else:
                        send_telegram_message("This Docker image was not being monitored.", chat_id)
                elif message_text.startswith('/list'):
                    if docker_images:
                        message = "Currently monitored Docker images:\n" + "\n".join([f"[{image}](https://hub.docker.com/r/{image})" for image in docker_images])
                        send_telegram_message(message, chat_id)
                    else:
                        send_telegram_message("No Docker images are currently being monitored.", chat_id)

if __name__ == "__main__":
    Thread(target=monitor_docker_images).start()
    handle_updates()
