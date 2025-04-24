FROM node:22.9.0

RUN apt-get update \
    && apt-get install -y wget supervisor gnupg  \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/agent1337 agent1337

WORKDIR /app

COPY package*.json ./
RUN npm install

ENV NODE_ENV=production

COPY src/ ./src/
COPY supervisord.conf /etc/supervisord.conf

RUN chown -R agent1337:agent1337 /app 


ENV SECRET_KEY=redactedl33tredactedl33t
ENV FLAG=HTB{FAKE_FLAG_FOR_TESTING}
ENV ADMIN_PASS=redactedl33t

RUN echo "$FLAG" > /flag.txt && chmod 644 /flag.txt

EXPOSE 5000

USER agent1337

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]