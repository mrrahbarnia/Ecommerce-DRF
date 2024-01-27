FROM python:3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Dependencies for install psycopg2
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y libpq-dev && \
    apt-get install -y musl-dev

COPY ./requirements.txt /app/requirements.txt

RUN mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./core /app