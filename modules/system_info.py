import os
import platform
import subprocess
from datetime import datetime

def get_os_info():
    """Recupera informaciÃ³n del sistema operativo y del kernel."""
    return {
        "OS": platform.system(),
        "Kernel Version": platform.release(),
        "Kernel Details": platform.version(),
        "Architecture": platform.architecture(),
        "Hostname": platform.node(),
    }

def check_sudo_version():
    """Verifica si el comando sudo estÃ¡ presente y muestra su versiÃ³n."""
    try:
        result = subprocess.run(['sudo', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.splitlines()[0] if result.returncode == 0 else "sudo no estÃ¡ disponible."
    except FileNotFoundError:
        return "sudo no estÃ¡ instalado en este sistema."
    except Exception as e:
        return f"Error al verificar sudo: {str(e)}"

def get_path_analysis():
    """Muestra las rutas del PATH y verifica su configuraciÃ³n."""
    paths = os.getenv("PATH", "").split(":")
    return {"PATH": paths, "Total Directories": len(paths)}

def get_time_and_date():
    """Muestra la hora y fecha actuales."""
    now = datetime.now()
    return {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
    }

def create_report_directory():
    """Crea la carpeta 'report' si no existe."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Recoge toda la informaciÃ³n del mÃ³dulo y la devuelve como un diccionario."""
    return {
        "os_info": get_os_info(),
        "sudo_version": check_sudo_version(),
        "path_analysis": get_path_analysis(),
        "time_and_date": get_time_and_date(),
    }

def generate_report(data, output_file="system_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        # Crear el directorio report
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w") as f:
            f.write("=== Informe de InformaciÃ³n del Sistema ===\n")
            
            f.write("\n--- InformaciÃ³n del Sistema Operativo ---\n")
            os_info = data.get("os_info", {})
            for key, value in os_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- VersiÃ³n de sudo ---\n")
            f.write(data.get("sudo_version", "No se pudo verificar sudo.\n"))
            
            f.write("\n--- AnÃ¡lisis de PATH ---\n")
            path_analysis = data.get("path_analysis", {})
            for key, value in path_analysis.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Hora y Fecha ---\n")
            time_date = data.get("time_and_date", {})
            for key, value in time_date.items():
                f.write(f"{key}: {value}\n")
        
        print(f"[+] Informe generado: {report_path}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
