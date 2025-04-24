FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-flask

WORKDIR /app

COPY webapp .
COPY notes.db .
COPY flag.txt .
COPY ext.so .

RUN useradd -m ctf
RUN chown -R ctf:ctf /app
USER ctf

EXPOSE 5000
CMD ["python3", "app.py"]
