FROM ubuntu:latest

RUN apt update && \
    apt install -y kea-dhcp4-server

COPY kea-dhcp4.conf /etc/kea/

CMD ["kea-dhcp4", "-c", "/etc/kea/kea-dhcp4.conf", "&"]
