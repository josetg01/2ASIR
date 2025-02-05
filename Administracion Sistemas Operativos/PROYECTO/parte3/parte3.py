import paramiko
import platform
import getpass

so = platform.system()

# Funciones de conexion remota
def conectar_ssh(hostname, port, username, password):
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
        hostname = input("Introduce la IP del equipo al que te conectas: ")
        port = input("Escribe el puerto de SSH de dicho equipo: ")
        username = input("Usuario con el que te conectas: ")
        password = getpass.getpass("Contraseña del usuario remoto: ")
        conectar_ssh(hostname, port, username, password)

# Funciones de gestión de impresión
def gestion_impresion():
    print("Función de gestión de impresión aún no implementada.")
    # Aquí podrías agregar código para gestionar impresoras, si es necesario

def menu():
    while True:
        print("1. Conectar a equipo remoto")
        print("2. Gestión de impresión")
        print("3. Salir")
        opcion = input("Introduce una opción [1-3]: ")
        
        if opcion == "1":
            conexion_remota()
        elif opcion == "2":
            gestion_impresion()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# Llamar al menú principal
menu()
