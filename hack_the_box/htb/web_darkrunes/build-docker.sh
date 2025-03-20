docker build --tag=web-darkrunes . && \
docker run -p 1337:3000 --rm --name=web-darkrunes -it web-darkrunes