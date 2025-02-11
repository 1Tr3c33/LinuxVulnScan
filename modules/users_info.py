import os
import subprocess

def list_users_and_groups():
    """Lista y categoriza todos los usuarios y grupos del sistema."""
    try:
        users = subprocess.getoutput("cut -d: -f1 /etc/passwd")
        groups = subprocess.getoutput("cut -d: -f1 /etc/group")
        return {
            "Users": users.splitlines(),
            "Groups": groups.splitlines(),
        }
    except Exception as e:
        return {"error": f"Error al listar usuarios y grupos: {str(e)}"}

def analyze_running_processes():
    """Analiza los procesos en ejecuciÃ³n en el sistema."""
    try:
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return "No se pudo listar los procesos. Puede requerir permisos root."
        return result.stdout
    except Exception as e:
        return f"Error al analizar procesos: {str(e)}"

def brute_su_check():
    """Verifica si el comando 'su' puede ser explotado."""
    try:
        if os.geteuid() != 0:
            return "El comando 'su' no puede verificarse sin privilegios root."
        
        result = subprocess.run(['su', '-c', 'echo Test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "El comando 'su' puede ser utilizado." if result.returncode == 0 else f"No se puede usar 'su': {result.stderr.strip()}"
    except Exception as e:
        return f"Error al verificar 'su': {str(e)}"

def analyze_user_access():
    """Analiza quÃ© usuarios tienen acceso al sistema."""
    try:
        active_users = subprocess.getoutput("who")
        return active_users.splitlines()
    except Exception as e:
        return {"error": f"Error al analizar los accesos de usuarios: {str(e)}"}

def check_last_logins():
    """Comprueba los Ãºltimos accesos al sistema."""
    try:
        result = subprocess.run(["last"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return "No se pudo acceder al historial de logins. Puede requerir permisos root."
        return result.stdout.splitlines()
    except Exception as e:
        return f"Error al comprobar Ãºltimos accesos: {str(e)}"

def create_report_directory():
    """Crea la carpeta 'report' si no existe."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Recoge toda la informaciÃ³n del mÃ³dulo y la devuelve como un diccionario."""
    return {
        "users_and_groups": list_users_and_groups(),
        "running_processes": analyze_running_processes(),
        "su_check": brute_su_check(),
        "user_access": analyze_user_access(),
        "last_logins": check_last_logins(),
    }

def generate_report(data, output_file="users_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        # Crear el directorio report
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w") as f:
            f.write("=== Informe de InformaciÃ³n de Usuarios ===\n")
            
            f.write("\n--- Usuarios y Grupos ---\n")
            users_groups = data.get("users_and_groups", {})
            for key, value in users_groups.items():
                f.write(f"{key}:\n" + "\n".join(value) + "\n")
            
            f.write("\n--- Procesos en EjecuciÃ³n ---\n")
            f.write(data.get("running_processes", "No se pudo obtener la informaciÃ³n de los procesos.\n"))
            
            f.write("\n--- VerificaciÃ³n de su ---\n")
            f.write(data.get("su_check", "No se pudo verificar el comando 'su'.\n"))
            
            f.write("\n--- Usuarios Activos ---\n")
            active_users = data.get("user_access", [])
            if isinstance(active_users, list):
                f.write("\n".join(active_users) + "\n")
            else:
                f.write(active_users + "\n")
            
            f.write("\n--- Ãšltimos Accesos ---\n")
            last_logins = data.get("last_logins", [])
            if isinstance(last_logins, list):
                f.write("\n".join(last_logins) + "\n")
            else:
                f.write(last_logins + "\n")
        
        print(f"[+] Informe generado: {report_path}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")

def check_root_privileges():
    """Verifica si el programa tiene privilegios de root."""
    if os.geteuid() != 0:
        print("[-] Advertencia: Algunos anÃ¡lisis pueden requerir permisos root para obtener resultados completos.")

if __name__ == "__main__":
    check_root_privileges()  # Verificar los privilegios antes de ejecutar
    data = gather_data()
    generate_report(data)
