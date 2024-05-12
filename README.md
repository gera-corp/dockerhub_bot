# Docker Image Monitoring Telegram Bot

This Telegram bot is designed to monitor Docker Hub for new tags on specified Docker images and notify a Telegram user when updates occur. It supports adding, removing, and listing Docker images for monitoring.

## Features

- **Monitor Docker Images**: Track new tags for specified Docker images.
- **Add Docker Images**: Dynamically add images to monitor via Telegram commands.
- **Remove Docker Images**: Remove images from the monitoring list.
- **List Monitored Images**: Get a list of all currently monitored Docker images.
- **Authorized User Control**: Only allow a specified Telegram user to control the bot.

## Environment Variables

To run this bot, you will need to set the following environment variables:

- `TELEGRAM_TOKEN`: Your Telegram Bot Token, which you can obtain from the [BotFather](https://t.me/botfather) on Telegram.
- `TELEGRAM_CHAT_ID`: You chat ID where bot send message.
- `AUTHORIZED_USER_ID`: The Telegram user ID that is authorized to control the bot. This must be set to the user's numeric ID.
- `CHECK_INTERVAL`: The interval in seconds as a string for how often the bot checks Docker Hub for new tags.
- `DATA_FILE`: Where will the databasefile be stored.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gera-corp/dockerhub_bot.git
   cd dockerhub_bot

2. **Install Dependencies**:
   ```bash
   pip3 install requests

3. **Set Environment Variables**:
   ```bash
   export TELEGRAM_TOKEN='your_bot_token_here'
   export TELEGRAM_CHAT_ID='you_chat_id'
   export AUTHORIZED_USER_ID='your_authorized_user_id'
   export CHECK_INTERVAL='3600'
   export DATA_FILE='data/docker_images.json'

4. **Run the Bot**:
   ```bash
   python3 main.py

## Available Commands
example:
```
    /add grafana/grafana
    /remove grafana/grafana
```
```
    /add <image_name> :Add a new Docker image to the monitoring list. Use the full repository name, e.g., library/nginx.
    /remove <image_name> :Remove an image from the monitoring list.
    /list :Display a list of all currently monitored Docker images.
```
## Development

Feel free to fork or contribute to this project. Pull requests are welcome for bug fixes, enhancements, or new features.
