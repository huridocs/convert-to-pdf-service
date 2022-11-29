FROM linuxserver/libreoffice:7.2.7 AS base
RUN apk --update add py3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY ./requirements/worker.txt worker.txt
COPY ./requirements/base.txt base.txt

RUN pip install --upgrade pip && pip install -r worker.txt && pip install --no-cache-dir newrelic

RUN mkdir -p /app
RUN mkdir -p /app/src
RUN mkdir -p /data
WORKDIR /app
COPY ./src/worker ./src

# ports and volumes
VOLUME /config

FROM base AS worker
WORKDIR /app/src
ENTRYPOINT python QueueProcessor.py
