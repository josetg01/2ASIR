#!/bin/bash

# Definir la ruta del archivo de log
LOGFILE="/var/log/monitorizacion.log"
DATE=$(TZ='Europe/Madrid' date +"%d-%m-%Y_%H:%M:%S")
LOGFILE_DATE="/var/log/monitorizacion""_""$DATE.log"

# Iniciar la supervisión y registrar el inicio del proceso
logger -t monitorizacion "[$(date)] Iniciando supervisión" >> $LOGFILE_DATE

# Supervisar el uso de la CPU y memoria, y registrar los procesos más consumidores
logger -t monitorizacion "[$(date)] Top 5 procesos que más CPU están utilizando:" >> $LOGFILE_DATE
ps aux --sort=-%cpu | head -n 6 | logger -t monitorizacion >> $LOGFILE_DATE

logger -t monitorizacion "[$(date)] Top 5 procesos que más memoria están utilizando:" >> $LOGFILE_DATE
ps aux --sort=-%mem | head -n 6 | logger -t monitorizacion >> $LOGFILE_DATE

# Supervisar el espacio en disco
logger -t monitorizacion "[$(date)] Revisión de espacio en disco:" >> $LOGFILE_DATE
df -h | grep -E '^/dev' | while read line; do
    used=$(echo $line | awk '{print $5}')
    used_percent=$(echo $used | sed 's/%//')
    if [[ $used_percent -gt 90 ]]; then
        echo "ALERTA: La partición $partition tiene menos de 10% de espacio libre." | logger -t monitorizacion >> $LOGFILE_DATE
    fi
done

# Supervisar los logs del sistema para errores
logger -t monitorizacion "[$(date)] Revisión de errores en syslog:" >> $LOGFILE_DATE
grep -i 'error' /var/log/syslog | tail -n 10 | logger -t monitorizacion >> $LOGFILE_DATE

logger -t monitorizacion "[$(date)] Revisión de errores en dmesg:" >> $LOGFILE_DATE
dmesg | grep -i 'error' | tail -n 10 | logger -t monitorizacion >> $LOGFILE_DATE

# Finalizar supervisión y registrar el final
logger -t monitorizacion "[$(date)] Supervisión completada" >> $LOGFILE_DATE

sudo -u logcheck logcheck -l $LOGFILE_DATE
cat $LOGFILE_DATE >> $LOGFILE
rm $LOGFILE_DATE
