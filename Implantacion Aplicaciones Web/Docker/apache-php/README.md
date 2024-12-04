# APACHE Y PHP en Docker
## Construir imagen
```
sudo docker build -t apache-php .
```
## ARRANCAR CONTENEDOR
```
sudo docker run -d --name apache-php -v /var/www/html:/var/www/html --net=host --restart=unless-stopped apache-php
```
## ARRANCAR CONTENEDOR CON DOCKER-COMPOSE
```
sudo docker compose up -d
```
