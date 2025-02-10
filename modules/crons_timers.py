import os
import subprocess


def analyze_running_processes():
    """Analiza los procesos en ejecución y el usuario que los ejecuta."""
    try:
        processes = subprocess.getoutput("ps aux")
        return processes
    except Exception as e:
        return f"Error al analizar los procesos en ejecución: {str(e)}"


def search_credential_processes():
    """Busca procesos que podrían almacenar credenciales en memoria."""
    try:
        suspicious_processes = subprocess.getoutput("ps aux | grep -i 'ssh\\|login\\|passwd\\|gpg\\|vault'")
        return suspicious_processes if suspicious_processes else "No se encontraron procesos sospechosos."
    except Exception as e:
        return f"Error al buscar procesos que podrían almacenar credenciales: {str(e)}"


def find_binaries_with_risky_permissions():
    """Busca binarios de procesos en ejecución con permisos inusuales."""
    try:
        risky_binaries = subprocess.getoutput("find /proc/*/exe -type f -exec ls -l {} \\; 2>/dev/null | grep 'rwx'")
        return risky_binaries if risky_binaries else "No se encontraron binarios con permisos inusuales."
    except Exception as e:
        return f"Error al buscar binarios con permisos riesgosos: {str(e)}"


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
    """Analiza timers configurados en el sistema a través de systemd."""
    try:
        timers = subprocess.getoutput("systemctl list-timers --all")
        return timers if timers else "No se encontraron timers configurados."
    except Exception as e:
        return f"Error al analizar timers en systemd: {str(e)}"


def generate_report(data, output_file="crons_timers_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Análisis de Procesos, Cron Jobs y Timers ===\n")
            f.write("\n--- Procesos en Ejecución ---\n")
            f.write(data.get("running_processes", "No se pudo obtener información sobre procesos.\n"))

            f.write("\n--- Procesos que podrían Almacenar Credenciales ---\n")
            f.write(data.get("credential_processes", "No se encontraron procesos sospechosos.\n"))

            f.write("\n--- Binarios con Permisos Inusuales ---\n")
            f.write(data.get("risky_binaries", "No se encontraron binarios con permisos inusuales.\n"))

            f.write("\n--- Cron Jobs ---\n")
            cron_jobs = data.get("cron_jobs", {})
            for job_type, jobs in cron_jobs.items():
                f.write(f"{job_type}:\n{jobs}\n")

            f.write("\n--- Systemd Timers ---\n")
            f.write(data.get("systemd_timers", "No se encontraron timers configurados.\n"))

        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "running_processes": analyze_running_processes(),
        "credential_processes": search_credential_processes(),
        "risky_binaries": find_binaries_with_risky_permissions(),
        "cron_jobs": analyze_cron_jobs(),
        "systemd_timers": analyze_systemd_timers(),
    }
    generate_report(data)