#!/bin/bash

# Definir la ubicación del script de monitoreo
SCRIPT_MONITOR="/etc/monitoreo.sh"
read -p "Introduce tu correo electronico de gmail para los logs: " email
read -s -p "Introduce tu contraseña del mail: " password_email
sudo apt update
sudo apt install logcheck msmtp msmtp-mta at -y
echo $password_email > /tmp/gmail_password.txt
gpg --output /etc/gmail_password.gpg --encrypt --armor --recipient $email /tmp/gmail_password.txt

# Verificar si el archivo de script ya existe, si no, descargarlo
if [ ! -f "$SCRIPT_MONITOR" ]; then
    echo "Descargando el script de monitoreo..."
    sudo wget https://raw.githubusercontent.com/josetg01/2ASIR/refs/heads/main/Administracion%20Sistemas%20Operativos/PROYECTO/parte2/monitoreo.sh -O "$SCRIPT_MONITOR"
    
    # Asegurarse de que el archivo descargado tenga permisos de ejecución
    sudo chmod +x "$SCRIPT_MONITOR"
else
    echo "El script de monitoreo ya existe en $SCRIPT_MONITOR. No es necesario descargarlo."
fi

#Programar una tarea puntual (por ejemplo, verificar si un servicio está corriendo) con at:
echo "systemctl is-active --quiet apache2 || systemctl restart apache2" | at 03:00

# Programar ejecucion automatica con crontab
sudo tee /etc/crontab >> /dev/null <<EOL
*/5 * * * *    bash $SCRIPT_MONITOR
EOL

# Crear el servicio systemd para el monitoreo
echo "Creando el servicio systemd para la supervisión..."
sudo tee /etc/systemd/system/monitorizacion.service > /dev/null <<EOL
[Unit]
Description=Servicio de supervisión del sistema
After=network.target

[Service]
ExecStart=/bin/bash $SCRIPT_MONITOR
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Recargar los servicios de systemd, habilitar e iniciar el servicio
echo "Habilitando e iniciando el servicio de monitoreo..."
sudo systemctl daemon-reload
sudo systemctl enable monitorizacion
sudo systemctl start monitorizacion

echo "El servicio de monitoreo está ahora activo y en ejecución."

#Configurar logcheck con sendmail y smtp de google
sudo tee /etc/msmtprc >> /dev/null <<EOL
# Configuración de msmtp para Gmail
account default
host smtp.gmail.com
port 587
from $email
user $email
password $(gpg --quiet --decrypt /etc/gmail_password.gpg)
tls on
tls_starttls on
auth on
logfile /var/log/msmtp.log
EOL
