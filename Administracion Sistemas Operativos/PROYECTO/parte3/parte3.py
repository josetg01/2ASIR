import paramiko
import platform

so = platform.system()


def conectar_ssh():
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

def windows_remote():

def conexion_remota():
  if so = "Windows":
    windows_remote()
  elif = "Linux":
def menu():
  print(1. Conectar a equipo remoto)
  print(2. Gestion de impresion)
  print(3. Salir)
  opcion = input("Introduce una opcion [1-3]:")
  if opcion = "1":
    
  elif
