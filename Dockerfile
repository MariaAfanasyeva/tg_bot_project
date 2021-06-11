FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code/
WORKDIR /code/
ADD requirements.txt /code/
COPY . /code/
EXPOSE 8000
RUN pip install -r requirements.txt
COPY . /code/
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
