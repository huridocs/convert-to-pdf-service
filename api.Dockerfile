FROM python:3.10.8-alpine

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements/api.txt api.txt
COPY ./requirements/base.txt base.txt
RUN pip install --upgrade pip && pip install -r api.txt && pip install --no-cache-dir newrelic

RUN mkdir /app
RUN mkdir /app/src
RUN mkdir /data
WORKDIR /app
COPY ./src/api ./src

WORKDIR /app/src
ENV FLASK_APP app.py

CMD gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:5050
