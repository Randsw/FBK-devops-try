FROM python:3.8.6-alpine3.12
LABEL maintainer="Andrew Rylik <rand@dep7mail.com>"

RUN apk update && apk upgrade && apk add postgresql-dev gcc python3-dev musl-dev

RUN python3 -m pip install --no-cache-dir psycopg2-binary

WORKDIR /code

EXPOSE 5432 8000

COPY scripts/http_server.py /code/http_server.py

COPY scripts/postgres_adapter.py /code/postgres_adapter.py