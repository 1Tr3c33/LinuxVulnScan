import os
import subprocess

def analyze_running_processes():
    """Analiza los procesos en ejecuciÃ³n y el usuario que los ejecuta."""
    try:
        processes = subprocess.getoutput("ps aux")
        return processes
    except Exception as e:
        return f"Error al analizar los procesos en ejecuciÃ³n: {str(e)}"

def search_credential_processes():
    """Busca procesos que podrÃ­an almacenar credenciales en memoria."""
    try:
        suspicious_processes = subprocess.getoutput("ps aux | grep -i 'ssh\\|login\\|passwd\\|gpg\\|vault'")
        return suspicious_processes if suspicious_processes else "No se encontraron procesos sospechosos."
    except Exception as e:
        return f"Error al buscar procesos que podrÃ­an almacenar credenciales: {str(e)}"

def analyze_cron_jobs():
    """Analiza tareas programadas en cron, anacron, incron y at."""
    try:
        cron_jobs = subprocess.getoutput("cat /etc/crontab; crontab -l 2>/dev/null; ls /etc/cron.d")
        anacron_jobs = subprocess.getoutput("ls /etc/anacrontab")
        incron_jobs = subprocess.getoutput("incrontab -l 2>/dev/null")
        at_jobs = subprocess.getoutput("atq")
        return {
            "Cron Jobs": cron_jobs,
            "Anacron Jobs": anacron_jobs,
            "Incron Jobs": incron_jobs,
            "At Jobs": at_jobs,
        }
    except Exception as e:
        return f"Error al analizar tareas programadas: {str(e)}"

def analyze_systemd_timers():
    """Analiza timers configurados en el sistema a travÃ©s de systemd."""
    try:
        timers = subprocess.getoutput("systemctl list-timers --all")
        return timers if timers else "No se encontraron timers configurados."
    except Exception as e:
        return f"Error al analizar timers en systemd: {str(e)}"

def create_report_directory():
    """Crea la carpeta 'report' si no existe."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Recoge toda la informaciÃ³n del mÃ³dulo y la devuelve como un diccionario."""
    return {
        "running_processes": analyze_running_processes(),
        "suspicious_processes": search_credential_processes(),
        "cron_jobs": analyze_cron_jobs(),
        "systemd_timers": analyze_systemd_timers(),
    }

def generate_report(data, output_file="crons_timers_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        # Crear el directorio report
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w") as f:
            f.write("=== Informe de Cron Jobs y Timers ===\n")
            
            f.write("\n--- Procesos en EjecuciÃ³n ---\n")
            f.write(data.get("running_processes", "No se pudo obtener la informaciÃ³n de los procesos.\n"))
            
            f.write("\n--- Procesos que podrÃ­an Almacenar Credenciales ---\n")
            f.write(data.get("suspicious_processes", "No se encontraron procesos sospechosos.\n"))
            
            f.write("\n--- Tareas Programadas ---\n")
            cron_jobs = data.get("cron_jobs", {})
            for key, value in cron_jobs.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Timers del Sistema ---\n")
            f.write(data.get("systemd_timers", "No se encontraron timers configurados.\n"))
        
        print(f"[+] Informe generado: {report_path}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
