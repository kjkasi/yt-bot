# yt-bot

docker build --pull --rm -f "Dockerfile" -t ytbot:latest "." 
docker run --rm --env TELEGRAM_TOKEN=ENTER_TOKEN ytbot
