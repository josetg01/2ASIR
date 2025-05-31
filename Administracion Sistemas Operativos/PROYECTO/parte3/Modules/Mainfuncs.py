# Librerías
import os
from Interface.ascii import test
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog

# Variable global para almacenar la impresora predeterminada
mainprinter = None 



# ------------------------- FUNCIONES PARA SISTEMA -------------------------
def getos():
    ostype = os.name

    if ostype == 'nt':
        return "windows"
    else:
        return "linux"

system = getos()

if system == "windows":
    try:
        import win32print
        import win32api
        import wmi
        color = "c"
    except ImportError:
        win32print = None
else:
    try:
        import cups
        color = "y"
    except ImportError:
        cups = None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------- FUNCIONES BÁSICAS IMPRESORAS -------------------------

# Función para obtener la impresora predeterminada
def mainprint():

    """Obtener impresora principal (solo una vez al inicio)"""

    if os.name == "nt" and win32print:
        mainprinter = win32print.GetDefaultPrinter()
    elif cups:
        conn = cups.Connection()
        mainprinter = conn.getDefault()
    else:
        mainprinter = None

    return mainprinter

# Función para listas impresoras
def list_printers():
    clear()
    """Función para mostrar las impresoras disponibles y permitir su selección."""
    printers_list = []

    # Detectar sistema operativo y obtener lista de impresoras
    if system == "windows":
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        printers_list = []
        
        # Obtener estado de cada impresora
        for printer in printers:
            printer_name = printer[2]
            handle = win32print.OpenPrinter(printer_name)
            printer_info = win32print.GetPrinter(handle, 2)  # Nivel 2 para obtener información detallada
            status = printer_info.get('Status', 'Desconocido')
            printers_list.append((printer_name, status))
    else:
        # Conectar al servidor de CUPS
        conn = cups.Connection()

        # Obtener la lista de impresoras
        printers = conn.getPrinters()

        printers_list = []

        # Obtener el estado de las impresoras
        for printer in printers:
            printer_name = printer
            status = printers[printer].get('printer-state', 'Desconocido')
            printers_list.append((printer_name, status))
    
    # Mostrar la lista de impresoras con su estado
    print("IMPRESORAS DISPONIBLES")
    for idx, (printer, status) in enumerate(printers_list, start=1):
        print(f"{idx}. {printer} - Estado: {status}")

    # Solicitar al usuario que seleccione una impresora
    option = input("Seleccione una impresora (número): ")
    try:
        option_num = int(option)
        if 1 <= option_num <= len(printers_list):
            selected_printer, _ = printers_list[option_num - 1]
            print(f"Seleccionaste: {selected_printer}")
            return selected_printer
        else:
            print("Número fuera de rango.")
    except ValueError:
        print("Entrada no válida")
# ------------------------- FUNCIONES PARA ADMINISTRAR IMPRESORAS -------------------------

# Función para establecer impresora como predeterminada
def set_default_printer(printer_name):
    """Establece la impresora como predeterminada."""
    try:
        if system == "windows":  # Windows
            win32print.SetDefaultPrinter(printer_name)
        else:  # Linux (CUPS)
            subprocess.run(["lpadmin", "-d", printer_name], check=True)
        
        print(f"La impresora '{printer_name}' ha sido establecida como predeterminada.")
    
    except Exception as e:
        print(f"Error al cambiar la impresora predeterminada: {e}")

# Función para imprimir una hoja de prueba
def print_test_page(printer_name):
    """Imprime una página de prueba con un mensaje personalizado."""
    print(f"Imprimiendo página de prueba en '{printer_name}'...")

    # Crear archivo de texto temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
        temp_file.write(test)
        test_file = temp_file.name  # Guardar el nombre del archivo

    try:
        if system == "windows":  # Windows
            subprocess.run(["notepad.exe", "/p", test_file], check=True)
        else:  # Linux (CUPS)
            subprocess.run(["lp", "-d", printer_name, test_file], check=True)
        
        print("Página de prueba enviada a la impresora.")

    except Exception as e:
        print(f"Error al imprimir página de prueba: {e}")

    finally:
        os.remove(test_file)  # Eliminar archivo temporal después de imprimir

# Función para iniciar una impresora pausada
def start_printer(printer_name):

    if system == "windows":
        print(f"Función no disponible para Windows")

    else:
        try:
            conn = cups.Connection()
            conn.enablePrinter(printer_name)
            print(f"Impresora habilitada correctamente")
        except Exception as e:
            print(f"Error: {e}")

# Función para detener una impresora
def stop_printer(printer_name):

    if system == "windows":
        print(f"Función no disponible para Windows")

    else:
        try:
            conn = cups.Connection()
            conn.disablePrinter(printer_name)
            print(f"Impresora deshabilitada correctamente")
            
        except Exception as e:
            print(f"Error: {e}")

# Función para eliminar una impresora
def remove_printer(printer_name):

    if system == "windows":
        print("Función no disponible para Windows")

    else:
        try:
            conn = cups.Connection()
            conn.deletePrinter(printer_name)
            print(f"Impresora deshabilitada correctamente")
            
        except Exception as e:
            print(f"Error: {e}")

# Función que muestra y maneja el submenú para la administración de impresoras
def manage_printers_submenu(printer_name):
    """Menú de administración de la impresora."""
    print("\nOpciones para la impresora seleccionada")
    print("1. Hacerla predeterminada")
    print("2. Imprimir página de prueba")
    
    if system != "windows":
        print("3. Iniciar impresora")
        print("4. Pausar impresora")

    print("5. Eliminar impresora")
    print("6. Cancelar")

    try:
        option = int(input("Selecciona una opción: "))

        if option == 1:
            set_default_printer(printer_name)
        elif option == 2:
            print_test_page(printer_name)
        elif option == 3:
            start_printer(printer_name)
        elif option == 4:
            stop_printer(printer_name)
        elif option == 5:
            remove_printer(printer_name)
        elif option == 6:
            print("Operación cancelada.")
        else:
            print("Opción no válida.")

    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")

# ------------------------- FUNCIONES PARA COLA DE IMPRESIÓN -------------------------

# Función para mostrar la cola de impresión de una impresora
def list_queue():
    if system == "windows":
        printer_name = win32print.GetDefaultPrinter()
        handle = win32print.OpenPrinter(printer_name)
        jobs = win32print.EnumJobs(handle, 0, 10, 1)
        
        if len(jobs) == 0:
            return "empty"
        else:
            for job in jobs:
                # Usar .get() para evitar KeyError y proporcionar un valor predeterminado
                job_id = job.get('JobId', 'N/A')
                status = job.get('Status', 'N/A')
                user_name = job.get('UserName', 'N/A')
                document = job.get('pDocument', 'N/A')
                
                print(f"Job ID: {job_id}, Estado: {status}, Usuario: {user_name}, Documento: {document}")
        
        win32print.ClosePrinter(handle)
    
    else:
        try: 
            conn = cups.Connection()
            jobs = conn.getJobs()

            if len(jobs) == 0:
                return "empty"
            else: 
                for job_id, job in jobs.items():
                    print(f"Job ID: {job_id}")
                    print(f"Usuario: {job.get('job-originating-user-name', 'Desconocido')}")
                    print(f"Nombre del trabajo: {job.get('title', 'Sin nombre')}")
                    print(f"Estado del trabajo: {job.get('job-state', 'Desconocido')}")
                    print(f"Impresora: {job.get('printer-uri', 'Desconocida')}")
                    print(f"Fecha: {job.get('time-at-creation', 'Desconocida')}")
                    print("---" * 40)

        except Exception as e:
            print(f"Error: {e}")

# Función para iniciar un trabajo de impresión
def start_job(job_id):
    if system == "windows":
        printer_name = win32print.GetDefaultPrinter()
        handle = win32print.OpenPrinter(printer_name)
        try:
            # Reanudar el trabajo de impresión usando SetJob
            win32print.SetJob(handle, job_id, 0, None, win32print.JOB_CONTROL_RESUME)
            print(f"Trabajo {job_id} reanudado correctamente.")
        except Exception as e:
            print(f"Error al reanudar el trabajo {job_id}: {e}")
        finally:
            win32print.ClosePrinter(handle)
    else:
        conn = cups.Connection()
        try:
            conn.restartJob(job_id)
            print(f"Trabajo {job_id} reanudado correctamente")
        except Exception as e:
            print(f"Error al reiniciar el trabajo {job_id}: {e}")

# Función para cancelar un trabajo de impresión
def cancel_job(job_id):
    if system == "windows":
        printer_name = win32print.GetDefaultPrinter()
        handle = win32print.OpenPrinter(printer_name)
        try:
            # Cancelar el trabajo usando SetJob

            win32print.SetJob(handle, job_id, 0, None, win32print.JOB_CONTROL_CANCEL)
            print(f"Trabajo {job_id} cancelado correctamente.")
        except Exception as e:
            print(f"Error al cancelar el trabajo {job_id}: {e}","r")
        finally:
            win32print.ClosePrinter(handle)    
    else:
        conn = cups.Connection()
        try:
            conn.cancelJob(job_id)
            print(f"Trabajo {job_id} cancelado correctamente")
        except Exception as e:
            print(f"Error al cancelar el trabajo {job_id}: {e}")

# Función para mostrar y manejar el menú de la cola de impresión
def manage_job_list_submenu(job_id):
    """ Submenú para trabajar con la cola de impresión """
    print("\nOpciones para el trabajo seleccionado")
    print("1. Reanudar trabajo")
    print("2. Cancelar trabajo")
    print("3. Cancelar")

    option = input("Introduce una opción: ")

    if option == "1":
        start_job(job_id)
    elif option == "2":
        cancel_job(job_id)
    elif option == "3":    
        return
    else:
        print("Opción no válida")
        
# ------------------------- FUNCIONES PARA IMPRESIÓN DE ARCHIVOS -------------------------

# Función para escoger un archivo de manera gráfica
def select_archive():
    """Abre un cuadro de diálogo para seleccionar un archivo PDF."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos PDF", "*.pdf"),("Todos los archivos", "*.*"))
    )
    root.destroy()  # Cierra la ventana de selección
    return archivo

# Función para imprimir cualquier documento
def print_document(defprinter, archivo):
    if system == "windows":

        # Enviar el archivo a la impresora utilizando win32api
        win32api.ShellExecute(
            0,
            "print",
            archivo,
            None,
            ".",
            0
        )
        print("Archivo enviado a imprimir correctamente")
    else:
        # Enviar el archivo PDF a la impresora utilizando lp
        subprocess.run(['lp', '-d', defprinter, archivo], capture_output=True, text=True)
        print("Archivo enviado a imprimir correctamente")
