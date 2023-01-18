FROM python:3.9-alpine

WORKDIR /usr/src/mock

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../requirements.txt .
RUN pip install -r requirements.txt
CMD python main.py