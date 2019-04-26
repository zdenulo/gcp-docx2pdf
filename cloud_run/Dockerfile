
FROM python:3.7-alpine


ENV APP_HOME /app

WORKDIR $APP_HOME

COPY app .

RUN pip install -r requirements.txt

RUN apk add libreoffice-base \
    libreoffice \
    openjdk8-jre


CMD ["/usr/local/bin/gunicorn", "--config", "gunicorn_config.py", "main:app"]
