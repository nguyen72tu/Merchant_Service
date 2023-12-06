FROM python:3.8

WORKDIR /app

COPY . /app

RUN apt-get update \
    && apt-get install -y python3-dev default-libmysqlclient-dev
RUN pip install -r requirements.txt
RUN python manage.py migrate

