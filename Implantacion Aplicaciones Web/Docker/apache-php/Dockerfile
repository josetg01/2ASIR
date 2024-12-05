FROM ubuntu:latest
RUN apt update && \
      apt upgrade -y \
      apt install \
      apache2 \
      libapache2-mod-php \
      php \
      php-mysql && \
      apt clean
CMD ["/etc/init.d/apache2", "start"]
