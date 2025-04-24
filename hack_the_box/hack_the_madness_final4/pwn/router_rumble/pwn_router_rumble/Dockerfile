FROM alpine:3.18

RUN addgroup -S ctf && adduser -S -G ctf ctf && \
    apk update && apk add socat qemu-aarch64

ADD --chown=ctf challenge/chall /home/ctf/
ADD --chown=ctf challenge/flag.txt /home/ctf/
RUN chmod 774 /home/ctf/chall

USER ctf
EXPOSE 1337
WORKDIR /home/ctf

ENTRYPOINT ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:qemu-aarch64 ./chall"]
