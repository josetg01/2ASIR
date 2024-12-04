# DNS BIND9 EN DOCKER
## Construir imagen
```
sudo docker build -t dns .
```
## ARRANCAR CONTENEDOR
```
sudo docker volume create dns
sudo docker run -d --name dns -v dns:/etc/bind -v /etc/bind/named.conf.local:/etc/bind/named.conf.local -v /var/lib/bind:/var/lib/bind --net=host --restart=unless-stopped dns
```
## ARRANCAR CONTENEDOR CON DOCKER-COMPOSE
```
sudo docker compose up -d
```
