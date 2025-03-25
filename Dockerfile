FROM python:3.13-slim-bullseye

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install psycopg2 && pip install -r requirements.txt

CMD ["sh", "-c", "chmod +x /app/scripts/* && /app/scripts/start.sh"]
