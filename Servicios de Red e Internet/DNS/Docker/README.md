# DNS BIND9 EN DOCKER
## Construir imagen
```
sudo docker build -t dns .
```
## ARRANCAR CONTENEDOR
```
sudo docker run -d --name dns -v /etc/bind:/etc/bind --net=host --restart=unless-stopped dns
```
