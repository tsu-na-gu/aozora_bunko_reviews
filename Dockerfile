FROM python:3.12.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
&& apt-get install gcc libpq-dev python3-dev netcat-traditional -y \
&& apt-get clean

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/

COPY ./.env /app/.env