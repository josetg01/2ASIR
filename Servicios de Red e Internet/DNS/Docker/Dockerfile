FROM ubuntu:latest
# Instalar BIND y utilidades
RUN apt update && apt install -y bind9 bind9-utils && apt-get clean
# Copiar la configuración de BIND
COPY named.conf /etc/bind
# Crear el directorio de datos de BIND y configurar permisos
RUN mkdir -p /var/lib/bind/ && chown bind:bind /var/lib/bind/
# Ejecutar el servicio BIND
CMD ["named", "-g"]
