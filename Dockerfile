# syntax=docker/dockerfile:1.1
FROM python:3.8-alpine
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install -r requirements.txt
RUN apk del .build-deps gcc musl-dev