import os
import platform
import getpass
import subprocess

so = platform.system()

if so == "Windows":
    import win32print
    import win32ui
elif so == "Linux" or so == "Darwin":
    import paramiko
    import cups

# Funciones de conexion remota
def conectar_ssh():
    hostname = input("Introduce la IP del equipo al que te conectas: ")
    port = input("Escribe el puerto de SSH de dicho equipo: ")
    username = input("Usuario con el que te conectas: ")
    password = getpass.getpass("Contraseña del usuario remoto: ")
    # Crear una instancia de un cliente SSH
    client = paramiko.SSHClient()

    # Cargar las claves del sistema
    client.load_system_host_keys()

    # Configuración para autoaceptar claves del servidor si es necesario
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectar al servidor SSH
        client.connect(hostname, port, username, password)

        print("Conexión SSH establecida. Puedes ejecutar comandos.")
        
        while True:
            # Solicitar al usuario un comando para ejecutar
            command = input("Introduce el comando que deseas ejecutar o 'exit' para salir: ")

            if command.lower() == 'exit':
                print("Cerrando sesión...")
                break
            
            # Ejecutar el comando remoto
            stdin, stdout, stderr = client.exec_command(command)
            
            # Mostrar la salida del comando
            print("Salida:")
            print(stdout.read().decode())

            # Mostrar posibles errores
            error = stderr.read().decode()
            if error:
                print("Error:")
                print(error)
    except Exception as e:
        print(f"Error al conectar: {e}")

    finally:
        # Cerrar la conexión
        client.close()

# Función para manejar la conexión remota en Windows
def windows_remote():
    print("Conexión remota en Windows (MSTSC).")
    hostname = input("Introduce la dirección IP del equipo al que te quieres conectar: ")
    username = input("Introduce tu nombre de usuario para la conexión: ")
    password = getpass.getpass("Introduce tu contraseña para la conexión: ")
    mstsc_command = f"mstsc /v:{hostname} /u:{username}"
    os.system(mstsc_command)
    print("Conexión remota establecida via MSTSC.")

def conexion_remota():
    if so == "Windows":
        windows_remote()
    elif so == "Linux":
        conectar_ssh()

# Funciones de gestión de impresión
def gestion_impresion():
    print("Función de gestión de impresión aún no implementada.")
    # Aquí podrías agregar código para gestionar impresoras, si es necesario

# Parte 2: Gestión de impresión

#Obtiene la impresora principal del sistema (en Windows y Linux).
def obtener_impresora_principal():
    so = platform.system()
    if so == "Windows":
        printer_name = win32print.GetDefaultPrinter()
        return printer_name
    elif so == "Linux" or so == "Darwin":
        # En Linux/Darwin usaremos lpstat para obtener la impresora predeterminada
        try:
            result = subprocess.check_output(['lpstat', '-d'])
            printer_name = result.decode('utf-8').split(":")[1].strip()
            return printer_name
        except subprocess.CalledProcessError:
            print("No se pudo obtener la impresora predeterminada.")
            return None

#Lista los trabajos de impresión en cola.
def listar_trabajos_impresion():
    so = platform.system()
    if so == "Windows":
        # Usamos la API de Windows para listar trabajos
        printer_name = obtener_impresora_principal()
        print(f"Trabajos de impresión en la impresora: {printer_name}")
        # Aquí se pueden obtener los trabajos usando win32print
        # Pero en este caso, mostramos un mensaje de ejemplo
        print("Listado de trabajos no implementado para Windows (requiere win32print).")
    elif so == "Linux" or so == "Darwin":
        print("Trabajos de impresión en cola (Linux/Darwin):")
        # Usamos lpstat en sistemas Unix-like
        try:
            result = subprocess.check_output(['lpstat', '-o'])
            print(result.decode('utf-8'))
        except subprocess.CalledProcessError:
            print("No se pudieron listar los trabajos de impresión.")

#Envía un archivo a la impresora.
def enviar_archivo_impresion():
    so = platform.system()
    file_path = input("Introduce la ruta del archivo a imprimir: ")
    
    if not os.path.exists(file_path):
        print("El archivo no existe.")
        return
    
    if so == "Windows":
        printer_name = obtener_impresora_principal()
        print(f"Enviando archivo a la impresora {printer_name}...")
        win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)
        print("Archivo enviado a impresión.")
    elif so == "Linux" or so == "Darwin":
        print(f"Enviando archivo a impresión...")
        try:
            subprocess.run(['lp', file_path])
            print("Archivo enviado a impresión.")
        except Exception as e:
            print(f"Error al enviar el archivo a la impresora: {e}")

#Cancela un trabajo de impresión.
def cancelar_trabajo_impresion():
    so = platform.system()
    if so == "Windows":
        # Usar la API de Windows para cancelar trabajos (requiere win32print)
        print("Cancelar trabajos en Windows no implementado.")
    elif so == "Linux" or so == "Darwin":
        job_id = input("Introduce el ID del trabajo de impresión a cancelar: ")
        try:
            subprocess.run(['cancel', job_id])
            print(f"Trabajo de impresión {job_id} cancelado.")
        except Exception as e:
            print(f"Error al cancelar el trabajo de impresión: {e}")

# Menú principal
def menu():
    while True:
        print("\nMenú de gestión:")
        print("1. Conexión remota")
        print("2. Gestión de impresión")
        print("3. Salir")
        opcion = input("Introduce una opción [1-3]: ")

        if opcion == "1":
            conexion_remota()
        elif opcion == "2":
            print("\nOpciones de impresión:")
            print("1. Ver trabajos de impresión")
            print("2. Enviar archivo a imprimir")
            print("3. Cancelar trabajo de impresión")
            print("4. Volver al menú principal")
            sub_opcion = input("Introduce una opción [1-4]: ")

            if sub_opcion == "1":
                listar_trabajos_impresion()
            elif sub_opcion == "2":
                enviar_archivo_impresion()
            elif sub_opcion == "3":
                cancelar_trabajo_impresion()
            elif sub_opcion == "4":
                continue
            else:
                print("Opción no válida.")
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# Ejecución del programa
# if __name__ == "__main__":
menu()
