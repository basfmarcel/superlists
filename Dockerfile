FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /superlists

COPY requirements.txt /superlists/
RUN pip install -r requirements.txt

COPY . /superlists/
