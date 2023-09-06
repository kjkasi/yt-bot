# yt-bot
# on dev machine
docker build --rm -t ytbot .
docker tag ytbot kjkasi/ytbot
docker push kjkasi/ytbot


# on server
docker pull kjkasi/ytbot
docker run -d --rm --env TELEGRAM_TOKEN=ENTER_TOKEN kjkasi/ytbot
