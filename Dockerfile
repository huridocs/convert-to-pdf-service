FROM python:3.11.1-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
	apt-get -y -q --no-install-recommends install \
    wget \
    cabextract \
    xfonts-utils \
    libreoffice \
    libreoffice-writer \
    ure \
    libreoffice-java-common \
    libreoffice-core \
    libreoffice-common \
    fonts-indic \
    fonts-noto \
    fonts-noto-cjk \
    fonts-arabeyes \
    fonts-kacst \
    fonts-freefont-ttf \
		openjdk-17-jre && \
	apt-get -y -q remove libreoffice-gnome && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN wget http://ftp.br.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.8_all.deb && \
    apt --fix-broken install -y ./ttf-mscorefonts-installer_3.8_all.deb && \
    rm ttf-mscorefonts-installer_3.8_all.deb && \
    fc-cache -f -v

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

COPY ./src ./src
