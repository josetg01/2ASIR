# DHCP EN DOCKER CON KEA
## Construir imagen
```
sudo docker build -t dhcp .
```
## ARRANCAR CONTENEDOR
```
sudo docker run -d --name dhcp -v /etc/kea:/etc/kea --net=host --restart=unless-stopped dhcp
```
## ARRANCAR CONTENEDOR CON DOCKER-COMPOSE
```
sudo docker compose up -d
```
