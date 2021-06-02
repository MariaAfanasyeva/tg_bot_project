FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /code/
WORKDIR /code/
ADD requirements.txt /code/
COPY . /code/
RUN pip install -r requirements.txt
ADD . /code/
