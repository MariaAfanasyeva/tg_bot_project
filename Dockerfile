# pull official base image
FROM python:3.8.3-alpine

# set work directory
FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /code/
WORKDIR /code/
ADD requirements.txt /code/
COPY . /code/
RUN pip install -r requirements.txt
ADD . /code/
