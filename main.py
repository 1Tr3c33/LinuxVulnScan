import sys

# Importar los módulos creados
from modules import container_info
from modules import crons_timers
from modules import interesting_files
from modules import network_info
from modules import perm_files
from modules import software_info
from modules import system_info
from modules import users_info


def display_help():
    """Muestra el panel de ayuda con información de los módulos."""
    help_text = """
    ==========================================
              Herramienta de Ciberseguridad
    ==========================================
    Opciones disponibles:
    1. Analizar contenedores (container_info).
    2. Analizar cron jobs y timers (crons_timers).
    3. Buscar archivos interesantes (interesting_files).
    4. Analizar información de red (network_info).
    5. Analizar permisos de archivos (perm_files).
    6. Analizar información de software (software_info).
    7. Analizar información del sistema (system_info).
    8. Analizar información de usuarios (users_info).
    9. Ejecutar todos los módulos (Análisis completo).
    10. Salir.

    Todos los resultados se guardarán en informes de texto plano generados automáticamente.
    """
    print(help_text)


def execute_module(module, module_name):
    """Ejecuta un módulo y genera su informe."""
    print(f"\n[+] Ejecutando {module_name}...")
    module.__name__
    module.main()
    print(f"[+] Módulo {module_name} ejecutado.\n")


def main():
    """Gestión principal de la aplicación."""
    while True:
        display_help()
        try:
            option = int(input("Seleccione una opción (1-10): "))
            
            if option == 1:
                execute_module(container_info, "Análisis de Contenedores")
            elif option == 2:
                execute_module(crons_timers, "Cron Jobs y Timers")
            elif option == 3:
                execute_module(interesting_files, "Archivos Interesantes")
            elif option == 4:
                execute_module(network_info, "Información de Red")
            elif option == 5:
                execute_module(perm_files, "Permisos de Archivos")
            elif option == 6:
                execute_module(software_info, "Información de Software")
            elif option == 7:
                execute_module(system_info, "Información del Sistema")
            elif option == 8:
                execute_module(users_info, "Información de Usuarios")
            elif option == 9:
                print("\n[+] Ejecutando todos los módulos...")
                execute_module(container_info, "Análisis de Contenedores")
                execute_module(crons_timers, "Cron Jobs y Timers")
                execute_module(interesting_files, "Archivos Interesantes")
                execute_module(network_info, "Información de Red")
                execute_module(perm_files, "Permisos de Archivos")
                execute_module(software_info, "Información de Software")
                execute_module(system_info, "Información del Sistema")
                execute_module(users_info, "Información de Usuarios")
                print("[+] Análisis completo finalizado.\n")
            elif option == 10:
                print("Saliendo de la aplicación. ¡Adiós!")
                sys.exit(0)
            else:
                print("[-] Opción no válida. Por favor, seleccione un número entre 1 y 10.")
        except ValueError:
            print("[-] Por favor, introduzca un número válido.")


if __name__ == "__main__":
    main()