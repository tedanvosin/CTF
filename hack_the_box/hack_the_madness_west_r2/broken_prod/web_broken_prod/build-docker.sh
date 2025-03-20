#!/bin/bash
docker build -t web_broken_prod .
docker run  --name=web_broken_prod --rm -p1337:80 -it web_broken_prod
