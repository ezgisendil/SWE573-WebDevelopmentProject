FROM python:3

ENV PYTHONUNBUFFERED=1

RUN mkdir /ServiceSearchProject

WORKDIR /ServiceSearchProject

ADD . /ServiceSearchProject/

COPY ./requirements.txt /ServiceSearchProject/requirements.txt

RUN pip install -r requirements.txt

COPY . /ServiceSearchProject
