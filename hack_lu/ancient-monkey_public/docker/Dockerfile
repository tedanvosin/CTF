FROM ubuntu@sha256:ab64a8382e935382638764d8719362bb50ee418d944c1f3d26e0c99fae49a345 AS builder

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Build readflag
WORKDIR /build
COPY readflag.c .
RUN gcc -o readflag -static readflag.c

# Build pacparser
RUN git clone https://github.com/manugarg/pacparser.git /pacparser \
    && cd /pacparser \
    && git checkout v1.4.1 \
    && cd src \
    && make \
    && echo "31f12bd24a845fd9eb856d94882def50ce536d13 pactester" | sha1sum -c \
    || (echo "Wrong pactester!"; sha1sum pactester; false)

FROM ubuntu@sha256:ab64a8382e935382638764d8719362bb50ee418d944c1f3d26e0c99fae49a345 AS runtime

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        socat \
    && rm -rf /var/lib/apt/lists/* \
    && echo "4e3cdad804e5cd12a3e165d41ae6b9b512e54cb1 /lib/x86_64-linux-gnu/libc.so.6" | sha1sum -c \
    || (echo "Wrong libc!"; sha1sum /lib/x86_64-linux-gnu/libc.so.6; false)

# Challenge files
COPY --from=builder --chown=root:root /build/readflag /readflag
COPY --from=builder --chown=root:root /pacparser/src/pactester /app/pactester
COPY --chown=root:root flag.txt /flag.txt
COPY --chown=root:root run.sh chal.sh proxy.pac /app/
RUN chmod +s /readflag \
    && chmod 400 /flag.txt

WORKDIR /app
CMD ["/app/run.sh"]
