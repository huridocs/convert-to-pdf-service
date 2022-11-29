FROM python:3.10.8-slim

RUN mkdir /app
RUN addgroup --system python && adduser --system --group python
RUN chown python:python /app
USER python

ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements/api.txt api.txt
COPY ./requirements/base.txt base.txt
RUN pip install --upgrade pip && pip install -r api.txt && pip install --no-cache-dir newrelic

COPY ./src/api /app
ENV FLASK_APP app.py

WORKDIR /app
CMD gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:5050
