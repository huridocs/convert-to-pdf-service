FROM python:3.11.0-slim-bullseye

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
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/data

RUN addgroup --system python && adduser --system --group python
RUN chown -R python:python /app
USER python

ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY ./requirements/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./src .
