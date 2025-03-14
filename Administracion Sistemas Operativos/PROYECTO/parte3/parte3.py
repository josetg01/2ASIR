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
            conn = cups.Connection()
            printer_name = conn.getDefault()
            return printer_name
        except Exception as e:
            print(f"Error al obtener la impresora predeterminada: {e}")
            return None

#Lista los trabajos de impresión en cola.
def listar_trabajos_impresion():
    so = platform.system()
    if so == "Windows":
        # Usamos la API de Windows para listar trabajos
        printer_name = obtener_impresora_principal()
        print(f"Trabajos de impresión en la impresora: {printer_name}")
        try:
            printer = win32print.OpenPrinter(printer_name)
            jobs = win32print.EnumJobs(printer, 0, -1, 1)
            if not jobs:
                print("No hay trabajos de impresión en la cola.")
            else:
                for job in jobs:
                    print(f"Trabajo ID: {job['JobId']}, Nombre de documento: {job['pDocument']}, Estado: {job['Status']}")
            win32print.ClosePrinter(printer)
        except Exception as e:
            print(f"Error al listar los trabajos de impresión: {e}")
    elif so == "Linux" or so == "Darwin":
        print("Trabajos de impresión en cola (Linux/Darwin):")
        # Usamos lpstat en sistemas Unix-like
        try:
            result = subprocess.run(['lpq'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error al listar los trabajos de impresión: {result.stderr}")
                return

            output = result.stdout.strip()
            if not output:
                print("No hay trabajos de impresión en la cola.")
            else:
                print(output)
        except Exception as e:
            print(f"Error al listar los trabajos de impresión: {e}")

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
            conn = cups.Connection()
            printer_name = obtener_impresora_principal()
            print(f"Enviando archivo a la impresora {printer_name}...")
            conn.printFile(printer_name, file_path, "Trabajo de impresión", {})
            print("Archivo enviado a impresión.")
        except Exception as e:
            print(f"Error al enviar el archivo a la impresora: {e}")

#Cancela un trabajo de impresión.
def cancelar_trabajo_impresion():
    so = platform.system()
    if so == "Windows":
        printer_name = obtener_impresora_principal()
        job_id = input("Introduce el ID del trabajo de impresión a cancelar: ")
        try:
            printer = win32print.OpenPrinter(printer_name)
            win32print.SetJob(printer, int(job_id), 0, None, win32print.JOB_CONTROL_DELETE)
            print(f"Trabajo de impresión {job_id} cancelado.")
            win32print.ClosePrinter(printer)
        except Exception as e:
            print(f"Error al cancelar el trabajo de impresión: {e}")
    elif so == "Linux" or so == "Darwin":
        job_id = input("Introduce el ID del trabajo de impresión a cancelar: ")
        try:
            conn = cups.Connection()
            conn.cancelJob(job_id)
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
