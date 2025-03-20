FROM node:22-alpine

# Install necessary packages
RUN apk add --update --no-cache supervisor

# setup app
RUN mkdir -p /app

# switch env
WORKDIR /app

# add app
COPY src .

# Copy flag
COPY flag.txt ./flag.txt

# install dependencies
RUN npm install

# copy configs
COPY conf/supervisord.conf /etc/supervisord.conf

# expose the server port
EXPOSE 1337

# run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]