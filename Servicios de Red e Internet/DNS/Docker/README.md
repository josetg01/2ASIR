## ARRANCAR CONTENEDOR
```
sudo docker run -d --name dns -v /etc/bind:/etc/bind --net=host --restart=unless-stopped dns
```
