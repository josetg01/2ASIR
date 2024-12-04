# APACHE Y PHP en Docker
## Construir imagen
```
sudo docker build -t apache-php .
```
## ARRANCAR CONTENEDOR
```
sudo docker run -d --name apache-php --net=host --restart=unless-stopped apache-php
```
## ARRANCAR CONTENEDOR CON DOCKER-COMPOSE
```
sudo docker compose up -d
```
