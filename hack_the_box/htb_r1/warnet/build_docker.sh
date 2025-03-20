#!/bin/sh
docker rm -f web_warnet
docker build -t web_warnet .
docker run --name=web_warnet --rm -p1337:1337 -it web_warnet