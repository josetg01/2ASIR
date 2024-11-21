FROM ubuntu:latest
RUN apt update && apt install -y mysql-server
COPY grant_privileges.sql /tmp
EXPOSE 3306/tcp
ENTRYPOINT []
