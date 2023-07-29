FROM node:20-alpine3.17



COPY lyceum/package.json /lyceum/package.json
COPY lyceum/static_dev/ /lyceum/static_dev/

RUN apk add --no-cache bash
RUN npm install tailwindcss -g live-server --no-progress
RUN npm run --prefix lyceum/ tailwind:build

WORKDIR /lyceum/


FROM python:3.9-alpine3.16

COPY ./project/ /lyceum/
WORKDIR /lyceum/
EXPOSE 8000


COPY project/requirements/basic-requirements.txt /temp/basic-requirements.txt
COPY project/requirements/dev-requirements.txt /temp/dev-requirements.txt
COPY project/requirements/test-requirements.txt /temp/test-requirements.txt


RUN pip3 install -r /temp/basic-requirements.txt
RUN pip3 install -r /temp/dev-requirements.txt
RUN pip3 install -r /temp/test-requirements.txt

RUN adduser --disabled-password lyceum-user

USER lyceum-user

