import platform
import subprocess
import sys

so = platform.system()
# Función para comprobar si la librería está instalada
def check_and_install(library):
    if so == "Linux":
        try:
            # Intentamos importar la librería
            __import__(library)
            print(f"La librería '{library}' ya está instalada.")
        except ImportError:
            # Si no está instalada, la instalamos
            print(f"La librería '{library}' no está instalada. Procediendo a instalar...")
            subprocess.run(["pip", "install", library, "--break-system-packages"])
    elif so == "Windows":
        try:
            # Intentamos importar la librería
            __import__(library)
            print(f"La librería '{library}' ya está instalada.")
        except ImportError:
            # Si no está instalada, la instalamos
            print(f"La librería '{library}' no está instalada. Procediendo a instalar...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])

# Lista de librerías que quieres comprobar e instalar
if so == "Linux":
    required_libraries = ['paramiko', 'pycups']
elif so == "Windows":
    required_libraries = ['pywin32', 'paramiko']

# Recorremos la lista de librerías
for lib in required_libraries:
    check_and_install(lib)
