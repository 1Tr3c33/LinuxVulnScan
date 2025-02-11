import sys

# Importar los mÃ³dulos creados
from modules import container_info
from modules import crons_timers
from modules import interesting_files
from modules import network_info
from modules import perm_files
from modules import software_info
from modules import system_info
from modules import users_info


def display_help():
    """Muestra el panel de ayuda con informaciÃ³n de los mÃ³dulos."""
    help_text = """
    ==========================================
                 Linux VulnScan
    ==========================================
    Opciones disponibles:
    1. Analizar contenedores (container_info).
    2. Analizar cron jobs y timers (crons_timers).
    3. Buscar archivos interesantes (interesting_files).
    4. Analizar informaciÃ³n de red (network_info).
    5. Analizar permisos de archivos (perm_files).
    6. Analizar informaciÃ³n de software (software_info).
    7. Analizar informaciÃ³n del sistema (system_info).
    8. Analizar informaciÃ³n de usuarios (users_info).
    9. Ejecutar todos los mÃ³dulos (AnÃ¡lisis completo).
    10. Salir.

    Todos los resultados se guardarÃ¡n en informes de texto plano generados automÃ¡ticamente.
    """
    print(help_text)


def execute_module(module, module_name):
    """Ejecuta un mÃ³dulo, recolecta los datos y genera su informe."""
    try:
        print(f"\n[+] Ejecutando {module_name}...")
        data = module.gather_data()  # Recoger datos del mÃ³dulo
        module.generate_report(data)  # Generar informe basado en los datos
        print(f"[+] MÃ³dulo {module_name} ejecutado con Ã©xito.\n")
    except AttributeError as e:
        print(f"[-] Error: El mÃ³dulo {module_name} no tiene la funciÃ³n esperada: {str(e)}")
    except Exception as e:
        print(f"[-] Error inesperado al ejecutar {module_name}: {str(e)}")


def main():
    """GestiÃ³n principal de la aplicaciÃ³n."""
    while True:
        display_help()
        try:
            option = int(input("Seleccione una opciÃ³n (1-10): "))
            
            if option == 1:
                execute_module(container_info, "AnÃ¡lisis de Contenedores")
            elif option == 2:
                execute_module(crons_timers, "Cron Jobs y Timers")
            elif option == 3:
                execute_module(interesting_files, "Archivos Interesantes")
            elif option == 4:
                execute_module(network_info, "InformaciÃ³n de Red")
            elif option == 5:
                execute_module(perm_files, "Permisos de Archivos")
            elif option == 6:
                execute_module(software_info, "InformaciÃ³n de Software")
            elif option == 7:
                execute_module(system_info, "InformaciÃ³n del Sistema")
            elif option == 8:
                execute_module(users_info, "InformaciÃ³n de Usuarios")
            elif option == 9:
                print("\n[+] Ejecutando todos los mÃ³dulos...")
                execute_module(container_info, "AnÃ¡lisis de Contenedores")
                execute_module(crons_timers, "Cron Jobs y Timers")
                execute_module(interesting_files, "Archivos Interesantes")
                execute_module(network_info, "InformaciÃ³n de Red")
                execute_module(perm_files, "Permisos de Archivos")
                execute_module(software_info, "InformaciÃ³n de Software")
                execute_module(system_info, "InformaciÃ³n del Sistema")
                execute_module(users_info, "InformaciÃ³n de Usuarios")
                print("[+] AnÃ¡lisis completo finalizado.\n")
            elif option == 10:
                print("Saliendo de la aplicaciÃ³n. Â¡AdiÃ³s!")
                sys.exit(0)
            else:
                print("[-] OpciÃ³n no vÃ¡lida. Por favor, seleccione un nÃºmero entre 1 y 10.")
        except ValueError:
            print("[-] Por favor, introduzca un nÃºmero vÃ¡lido.")


if __name__ == "__main__":
    main()
