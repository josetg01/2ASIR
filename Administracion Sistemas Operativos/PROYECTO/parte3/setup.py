import subprocess
import sys

so = platform.system()

# Lista de librerías que quieres comprobar e instalar
if so == "Linux":
    required_libraries = ['paramiko', 'cups']
elif so == "Windows":
    required_libraries = ['win32print', 'win32ui']
    import win32print
# Función para comprobar si la librería está instalada
def check_and_install(library):
    try:
        # Intentamos importar la librería
        __import__(library)
        print(f"La librería '{library}' ya está instalada.")
    except ImportError:
        # Si no está instalada, la instalamos
        print(f"La librería '{library}' no está instalada. Procediendo a instalar...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])

# Recorremos la lista de librerías
for lib in required_libraries:
    check_and_install(lib)
