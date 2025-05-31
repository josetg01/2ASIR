# Librerías
from Interface.ascii import g_main
from Modules.Mainfuncs import *

# Obtener datos de funciones 
system = getos() # Sistema
 
# Variable menu
option = "0"

if system == "windows":
    color = "c"
else:
    color = "y"

# Desplegar opciones
def options():

    """ Función para mostrar opciones en el menú principal 
        y no repetir código """
    
    print("\n1. Administrar impresoras")
    print("2. Gestionar trabajos de impresión")
    print("3. Imprimir archivos\n")
    print("Exit para salir y clear para limpiar la pantalla\n")


# Menú principal
def main_menu():
    print(g_main)
    print(f"Sistema en uso: {(system)}")
    print(f"Impresora principal: {(mainprint())}")
   

if __name__ == "__main__":
    # Flujo principal
    try:

        while option != "exit":

            main_menu()
            options()

            option = input("Introduce una opción (1-3): ")

            if option == "1":
                print("\nADMINISTRACIÓN DE IMPRESORAS\n")
                selectprinter = list_printers() # Esta función lista todas las impresoras y nos permite manejarlas
                manage_printers_submenu(selectprinter)

            elif option == "2":
                print("\nGESTIONAR COLA DE IMPRESIÓN")
                empty = list_queue()
                if empty == "empty":
                    print("No hay trabajos para administrar")
                else:
                    jobid = int(input("Introduce el trabajo que deseas administrar: "))
                    manage_job_list_submenu(jobid, mainprinter)


            elif option == "3":
                print("\nIMPRIMIR ARCHIVOS\n")
                archivo = select_archive()
                printerrr = list_printers()
                set_default_printer(printerrr)
                print_document(printerrr, archivo)

            elif option == "clear":
                clear()

            elif option == "exit":
                print("\nByeee !!")

            else:
                print("\nOpción no válida")

    except KeyboardInterrupt:
        print("\nByeee !!")