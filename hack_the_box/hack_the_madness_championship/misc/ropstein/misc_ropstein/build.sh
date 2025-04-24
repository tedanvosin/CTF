#!/bin/bash
docker rm -f  ropstein
docker build --platform linux/amd64 -t ropstein . 

docker run --platform linux/amd64 --name=ropstein --rm -p1337:5000 -it ropstein
