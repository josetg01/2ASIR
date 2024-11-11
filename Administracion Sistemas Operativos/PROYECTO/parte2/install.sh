#!/bin/bash
SCRIPT_MONITOR="/etc/monitoreo.sh"
#SCRIPT DE MONITOREO
sudo wget https://raw.githubusercontent.com/josetg01/2ASIR/refs/heads/main/Administracion%20Sistemas%20Operativos/PROYECTO/parte2/monitoreo.sh -O $SCRIPT_MONITOR

#Establecimiento del servicio de monitoreo
cat > /etc/systemd/system/monitorizacion.service <<EOL
[Unit]
Description=Servicio de supervisión del sistema
After=network.target

[Service]
ExecStart=$SCRIPT_MONITOR
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl enable monitorizacion
sudo systemctl start monitorizacion
