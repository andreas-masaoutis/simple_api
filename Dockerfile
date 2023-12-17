FROM python:3.9

WORKDIR /simple_api

COPY /requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
