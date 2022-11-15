FROM lsiobase/rdesktop-web:alpine AS base

# set version label
ARG BUILD_DATE
ARG VERSION
ARG LIBREOFFICE_VERSION

LABEL build_version="convert-to-pdf version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="HURIDOCS"

RUN echo "**** preparing Python ****"
RUN apk --update add python3 py3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN echo "**** install requirements ****"
COPY src/worker/requirements/base.txt base.txt
RUN pip install --upgrade pip
RUN pip install -r base.txt

# Original Libreoffice script
RUN \
  echo "**** install packages ****" && \
  apk add --no-cache --virtual=build-dependencies \
    curl && \
  if [ -z ${LIBREOFFICE_VERSION+x} ]; then \
    LIBREOFFICE_VERSION=$(curl -sL "http://dl-cdn.alpinelinux.org/alpine/v3.15/community/x86_64/APKINDEX.tar.gz" | tar -xz -C /tmp \
    && awk '/^P:libreoffice$/,/V:/' /tmp/APKINDEX | sed -n 2p | sed 's/^V://'); \
  fi && \
  apk add --no-cache \
    libreoffice==${LIBREOFFICE_VERSION} \
    openjdk8-jre \
    tint2 && \
  echo "**** openbox tweaks ****" && \
  sed -i \
    's/NLMC/NLIMC/g' \
    /etc/xdg/openbox/rc.xml && \
  echo "**** cleanup ****" && \
  apk del --purge \
    build-dependencies && \
  rm -rf \
    /tmp/*

# add local libreoffice files
COPY /root /

# add local service files
RUN mkdir -p /app
RUN mkdir -p /app/src
RUN mkdir -p /data
WORKDIR /app
COPY ./src/worker ./src

# ports and volumes
VOLUME /config

FROM base AS worker
WORKDIR /app/src
CMD python QueueProcessor.py
