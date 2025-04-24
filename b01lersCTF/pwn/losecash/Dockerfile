FROM ubuntu:22.04@sha256:d80997daaa3811b175119350d84305e1ec9129e1799bba0bd1e3120da3ff52c3 AS base

FROM pwn.red/jail

COPY --from=base / /srv
COPY ./lose_cash /srv/app/run
COPY ./flag.txt /srv/app/
ENV JAIL_TIME=60 JAIL_MEM=100M JAIL_PORT=7777 JAIL_CPU=1000
