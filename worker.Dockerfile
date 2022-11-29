FROM python:3.10.8-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
	apt-get -y -q --no-install-recommends install \
		libreoffice \
		libreoffice-writer \
		ure \
		libreoffice-java-common \
		libreoffice-core \
		libreoffice-common \
		openjdk-17-jre && \
	apt-get -y -q remove libreoffice-gnome && \
	apt -y autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/data

RUN addgroup --system python && adduser --system --group python
RUN chown -R python:python /app
USER python

ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements/worker.txt worker.txt
COPY ./requirements/base.txt base.txt

RUN pip install --upgrade pip && pip install -r worker.txt && pip install --no-cache-dir newrelic

COPY ./src/worker /app

WORKDIR /app
ENTRYPOINT python QueueProcessor.py
