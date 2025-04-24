#!/bin/bash

# Stop and remove existing container
docker stop  eyes-in-the-sky-container || true
docker rm  eyes-in-the-sky-container || true

# Remove existing image
docker rmi eyes-in-the-sky || true

# Build new image
docker build -t  eyes-in-the-sky .

# Run new container
docker run \
  --name  eyes-in-the-sky-container \
  -p 3000:3000 \
   eyes-in-the-sky

echo "Challenge started!"