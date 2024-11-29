#!/bin/bash
read -p "Introduce la contraseña a usar en el listener de oracle-xe 21c: " pass_oracle

# Actualizacion de Oracle Linux
dnf -y update

# Instalacion y preparacion de Oracle Linux para instalar Oracle Xe 21c 
curl -o oracle-database-preinstall-21c-1.0-1.el8.x86_64.rpm https://yum.oracle.com/repo/OracleLinux/OL8/appstream/x86_64/getPackage/oracle-database-preinstall-21c-1.0-1.el8.x86_64.rpm
dnf -y localinstall oracle-database-preinstall-21c-1.0-1.el8.x86_64.rpm

# Instalacion de Oracle Xe 21c
curl -o oracle-database-xe-21c-1.0-1.ol8.x86_64.rpm https://download.oracle.com/otn-pub/otn_software/db-express/oracle-database-xe-21c-1.0-1.ol8.x86_64.rpm
dnf -y localinstall oracle-database-preinstall-21c-1.0-1.el8.x86_64.rpm

# Configuracion del listener
(echo $pass_oracle; echo $pass_oracle;) | /etc/init.d/oracle-xe-21c configure >> /xe_logs/XEsilentinstall.log 2>&1

# Activacion del servicio
systemctl daemon-reload
systemctl enable oracle-xe-21c
systemctl start oracle-xe-21c
