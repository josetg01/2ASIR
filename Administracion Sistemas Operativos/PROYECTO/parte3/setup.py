import subprocess
import sys

# Lista de librerías que quieres comprobar e instalar
required_libraries = ['numpy', 'pandas', 'requests']

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
