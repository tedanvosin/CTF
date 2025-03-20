FROM node:16.5.0

COPY flag.txt /flag.txt
WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY ./src ./src
COPY ./views ./views
COPY ./static ./static

ENV PORT 3000
EXPOSE $PORT

ENV OPENSSL_CONF=/dev/null

CMD ["npm", "start"]
