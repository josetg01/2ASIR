#!/bin/bash

# Definir la ruta del archivo de log
LOGFILE="/var/log/monitorizacion.log"
DATE=$(TZ='Europe/Madrid' date +"%d-%m-%Y_%H:%M:%S")
LOGFILE_FILE="$LOGFILE_$DATE

# Iniciar la supervisión y registrar el inicio del proceso
logger -t monitorizacion "[$(date)] Iniciando supervisión" >> $LOGFILE

# Supervisar el uso de la CPU y memoria, y registrar los procesos más consumidores
logger -t monitorizacion "[$(date)] Top 5 procesos que más CPU están utilizando:" >> $LOGFILE
ps aux --sort=-%cpu | head -n 6 | logger -t monitorizacion >> $LOGFILE

logger -t monitorizacion "[$(date)] Top 5 procesos que más memoria están utilizando:" >> $LOGFILE
ps aux --sort=-%mem | head -n 6 | logger -t monitorizacion >> $LOGFILE

# Supervisar el espacio en disco
logger -t monitorizacion "[$(date)] Revisión de espacio en disco:" >> $LOGFILE
df -h | grep -E '^/dev' | while read line; do
    used=$(echo $line | awk '{print $5}')
    used_percent=$(echo $used | sed 's/%//')
    # if [[ "${available%?}" -lt 10 ]]; then
    if [[ $used_percent -gt 90 ]]; then
        echo "ALERTA: La partición $partition tiene menos de 10% de espacio libre." | logger -t monitorizacion >> $LOGFILE
    fi
done

# Supervisar los logs del sistema para errores
logger -t monitorizacion "[$(date)] Revisión de errores en syslog:" >> $LOGFILE
grep -i 'error' /var/log/syslog | tail -n 10 | logger -t monitorizacion >> $LOGFILE

logger -t monitorizacion "[$(date)] Revisión de errores en dmesg:" >> $LOGFILE
dmesg | grep -i 'error' | tail -n 10 | logger -t monitorizacion >> $LOGFILE

# Finalizar supervisión y registrar el final
logger -t monitorizacion "[$(date)] Supervisión completada" >> $LOGFILE

sudo -u logcheck logcheck -l $LOGFILE
