FROM python:3.12-alpine
ADD . /app
WORKDIR /app
RUN apk add ffmpeg
RUN python -m pip install -r requirements.txt
WORKDIR /app/src
CMD ["python3", "main.py"]