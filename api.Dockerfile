FROM python:3.9-alpine AS base

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY src/api/requirements/base.txt base.txt
RUN pip install --upgrade pip
RUN pip install -r base.txt

RUN mkdir /app
RUN mkdir /app/src
RUN mkdir /data
WORKDIR /app
COPY ./src/api ./src

FROM base AS api
WORKDIR /app/src
ENV FLASK_APP app.py
CMD gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:5050