FROM node:16

WORKDIR /usr/src/app
COPY ./package.json ./
RUN npm install

COPY . .
RUN npm run dev
CMD ["npm", "run", "start"]

FROM python:3.9-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ../requirements.txt .
RUN pip install -r requirements.txt
