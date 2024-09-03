FROM python:3.12-bullseye

RUN mkdir /sqlite-web
WORKDIR /sqlite-web
COPY . /sqlite-web

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH