FROM node:alpine

# Install necessary packages
RUN apk add --no-cache \
    supervisor 

WORKDIR /app

COPY ./src /app/

RUN npm install

COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["/entrypoint.sh"]
