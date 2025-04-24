#!/bin/sh

docker run -p 1337:1337 $(docker build -q .)
