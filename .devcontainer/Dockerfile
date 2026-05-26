FROM python:3.12-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk add git gcc musl-dev libffi-dev

WORKDIR /workspace