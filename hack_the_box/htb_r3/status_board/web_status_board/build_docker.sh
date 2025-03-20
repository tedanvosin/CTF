#!/bin/bash
docker rm -f web_status_board
docker build -t web_status_board . && \
docker run --name=web_status_board --rm -p1337:80 -it web_status_board