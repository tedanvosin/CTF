#!/bin/bash
docker rm -f timetok
docker build -t timetok . && \
docker run --name=timetok --rm -p1337:80 -it timetok