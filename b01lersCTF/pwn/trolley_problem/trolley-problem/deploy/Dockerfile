# Standard debian instance, pin specific version to avoid breaking libc changes and such
FROM --platform=linux/amd64 debian@sha256:4abf773f2a570e6873259c4e3ba16de6c6268fb571fd46ec80be7c67822823b3 AS safe_trolley-problem_inner_container

RUN apt-get update && \
apt-get install -y socat

# wrapper.sh wraps the executable by
# performing any necessary setup
# this has to be called /app/run for redpwn jail to work
COPY ./deploy/wrapper.sh /app/run
RUN chmod +x /app/run

COPY ./src/chall /app/chall
RUN chmod +x /app/chall

COPY ./flag.txt /app/flag.txt

# this container runs the redpwn jail
FROM pwn.red/jail

# copy challenge container files to /srv
# /srv will be all files in the jail
COPY --from=safe_trolley-problem_inner_container / /srv

# configures allowed memory in redpwn jail
ENV JAIL_MEM=10M
# configures time before chall is killed
ENV JAIL_TIME=1800
# use specified port to run challenge
ENV JAIL_PORT=1337
