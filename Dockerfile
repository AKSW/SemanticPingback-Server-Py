FROM python:3

LABEL maintainer="Natanael Arndt <arndtn@gmail.com>"

RUN useradd -md /usr/src/app flask
USER flask
WORKDIR /usr/src/app

COPY templates/ /usr/src/app/templates
COPY pingback_server.py /usr/src/app/
COPY requirements.txt /usr/src/app/

USER root
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir uwsgi

RUN touch links.ttl && chown flask links.ttl

USER flask

EXPOSE 8080
#CMD uwsgi --plugins python3 --http-socket 0.0.0.0:8080 --module pingback_server --callable app
CMD uwsgi --http 0.0.0.0:8080 --module pingback_server --callable app
