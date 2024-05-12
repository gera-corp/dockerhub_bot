FROM python:alpine3.19

# telegram bot token
ENV TELEGRAM_TOKEN=""
# telegram chat id
ENV TELEGRAM_CHAT_ID=""
# telegram authorized user id
ENV AUTHORIZED_USER_ID=""
# check interval in seconds
ENV CHECK_INTERVAL="3600"
# whete is store datafile
ENV DATA_FILE="data/docker_images.json"

RUN mkdir -p /bot/data
WORKDIR /bot
COPY bot/* .
RUN pip3 install requests

CMD ["python3", "main.py"]
