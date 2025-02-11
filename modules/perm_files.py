import subprocess
import os

def analyze_suid_files():
    """Analiza archivos con el bit SUID habilitado."""
    try:
        suid_files = subprocess.getoutput("find / -perm -4000 -type f 2>/dev/null")
        return suid_files if suid_files else "No se encontraron archivos con SUID habilitado."
    except Exception as e:
        return f"Error al analizar archivos SUID: {str(e)}"

def analyze_sgid_files():
    """Analiza archivos con el bit SGID habilitado."""
    try:
        sgid_files = subprocess.getoutput("find / -perm -2000 -type f 2>/dev/null")
        return sgid_files if sgid_files else "No se encontraron archivos con SGID habilitado."
    except Exception as e:
        return f"Error al analizar archivos SGID: {str(e)}"

def analyze_acl_files():
    """Analiza archivos con ACLs configuradas y selecciona los mÃ¡s relevantes."""
    try:
        command = ("getfacl -R / 2>/dev/null | grep 'file:' | "
                   "grep -E '/etc|/home|/var|/usr' | sort -u")
        acl_files = subprocess.getoutput(command)
        filtered_files = "\n".join(acl_files.splitlines()[:100])  # Limitar a 100 resultados
        return filtered_files if filtered_files else "No se encontraron archivos clave con ACLs configuradas."
    except Exception as e:
        return f"Error al analizar archivos con ACLs: {str(e)}"

def analyze_capabilities():
    """Analiza capacidades configuradas en el sistema para procesos y archivos."""
    try:
        capabilities = subprocess.getoutput("getcap -r / 2>/dev/null")
        return capabilities if capabilities else "No se encontraron capacidades configuradas."
    except Exception as e:
        return f"Error al analizar capacidades: {str(e)}"

def analyze_service_permissions():
    """Detecta configuraciones peligrosas en directorios relacionados con servicios del sistema."""
    try:
        risky_directories = subprocess.getoutput("find /etc/systemd/system /lib/systemd/system -type d -perm -o+w 2>/dev/null")
        return risky_directories if risky_directories else "No se encontraron directorios con permisos peligrosos."
    except Exception as e:
        return f"Error al analizar permisos de servicios: {str(e)}"

def create_report_directory():
    """Crea la carpeta 'report' si no existe."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Recoge toda la informaciÃ³n del mÃ³dulo y la devuelve en un diccionario."""
    return {
        "suid_files": analyze_suid_files(),
        "sgid_files": analyze_sgid_files(),
        "acl_files": analyze_acl_files(),
        "capabilities": analyze_capabilities(),
        "risky_service_permissions": analyze_service_permissions(),
    }

def generate_report(data, output_file="perm_files_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        # Crear el directorio report
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w") as f:
            f.write("=== Informe de Permisos de Archivos ===\n")
            
            f.write("\n--- Archivos con SUID ---\n")
            f.write(data.get("suid_files", "No se encontraron archivos con SUID habilitado.\n"))
            
            f.write("\n--- Archivos con SGID ---\n")
            f.write(data.get("sgid_files", "No se encontraron archivos con SGID habilitado.\n"))
            
            f.write("\n--- Archivos Clave con ACLs Configuradas ---\n")
            f.write(data.get("acl_files", "No se encontraron archivos clave con ACLs configuradas.\n"))
            
            f.write("\n--- Capacidades Configuradas ---\n")
            f.write(data.get("capabilities", "No se encontraron capacidades configuradas.\n"))
            
            f.write("\n--- Permisos Peligrosos en Servicios ---\n")
            f.write(data.get("risky_service_permissions", "No se encontraron directorios con permisos peligrosos.\n"))

        print(f"[+] Informe generado: {report_path}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
