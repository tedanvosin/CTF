#!/bin/sh

docker build -t trojans-trojan .
docker run -p5000:5000 trojans-trojan
