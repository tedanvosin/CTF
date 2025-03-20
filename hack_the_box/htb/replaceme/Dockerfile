FROM ubuntu:20.04

RUN apt update --fix-missing && \
    apt install -y socat && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r ctf -g 1337 && useradd -r -g ctf -u 1337 ctf

WORKDIR /home/ctf

COPY challenge/flag.txt .
COPY challenge/replaceme .

RUN chmod +x replaceme

USER ctf
EXPOSE 1337
CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./replaceme"]
