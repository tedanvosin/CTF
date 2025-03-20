#!/bin/bash
docker build -t web_ioi_vault .
docker run --name=web_ioi_vault --rm -p1337:1337 -it web_ioi_vault
