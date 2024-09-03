FROM python:3.12-bullseye

RUN mkdir /app
WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app:$PYTHONPATH

RUN pip install -r requirements.txt
