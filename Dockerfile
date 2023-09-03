FROM python:3.11-alpine
ENV TELEGRAM_TOKEN=""
CMD ["sh", "-c", "python", TELEGRAM_TOKEN]