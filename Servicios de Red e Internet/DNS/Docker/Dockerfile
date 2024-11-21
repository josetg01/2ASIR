FROM ubuntu:latest
RUN apt update && apt install -y bind9 bind9-utils
COPY named.conf /etc/bind
RUN mkdir -p /var/lib/bind/
CMD["named", "-g"]
