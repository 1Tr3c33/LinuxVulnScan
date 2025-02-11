import os
import subprocess

def list_shell_scripts_in_path():
    """Enumera archivos .sh en los directorios definidos en la variable PATH."""
    try:
        paths = os.getenv("PATH", "").split(":")
        shell_scripts = []
        for path in paths:
            shell_scripts += subprocess.getoutput(f"find {path} -name '*.sh' 2>/dev/null").splitlines()
        return shell_scripts if shell_scripts else "No se encontraron scripts .sh en los directorios PATH."
    except Exception as e:
        return f"Error al buscar scripts .sh: {str(e)}"

def find_broken_symlinks():
    """Identifica enlaces simbÃ³licos rotos en los directorios PATH."""
    try:
        paths = os.getenv("PATH", "").split(":")
        broken_symlinks = []
        for path in paths:
            broken_symlinks += subprocess.getoutput(f"find {path} -xtype l 2>/dev/null").splitlines()
        return broken_symlinks if broken_symlinks else "No se encontraron enlaces simbÃ³licos rotos."
    except Exception as e:
        return f"Error al buscar enlaces simbÃ³licos rotos: {str(e)}"

def find_sensitive_php_configs():
    """Busca contraseÃ±as o configuraciones sensibles en archivos PHP."""
    try:
        php_files = subprocess.getoutput("grep -iR 'password\\|db_' /var/www 2>/dev/null")
        return php_files if php_files else "No se encontraron configuraciones sensibles en archivos PHP."
    except Exception as e:
        return f"Error al analizar archivos PHP: {str(e)}"

def find_backup_directories_and_files():
    """Busca directorios y archivos de respaldo."""
    try:
        backup_dirs = subprocess.getoutput("find / -type d -name '*backup*' 2>/dev/null")
        backup_files = subprocess.getoutput("find / -type f -name '*.bak' -o -name '*.backup' 2>/dev/null")
        return {
            "Backup Directories": backup_dirs if backup_dirs else "No se encontraron directorios de respaldo.",
            "Backup Files": backup_files if backup_files else "No se encontraron archivos de respaldo.",
        }
    except Exception as e:
        return f"Error al buscar respaldos: {str(e)}"

def create_report_directory():
    """Crea la carpeta 'report' si no existe."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Recoge toda la informaciÃ³n del mÃ³dulo y la devuelve como un diccionario."""
    return {
        "shell_scripts": list_shell_scripts_in_path(),
        "broken_symlinks": find_broken_symlinks(),
        "php_configs": find_sensitive_php_configs(),
        "backups": find_backup_directories_and_files(),
    }

def generate_report(data, output_file="interesting_files_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        # Crear el directorio report
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w") as f:
            f.write("=== Informe de Archivos Interesantes ===\n")
            
            f.write("\n--- Scripts .sh en PATH ---\n")
            shell_scripts = data.get("shell_scripts", [])
            if isinstance(shell_scripts, list):
                f.write("\n".join(shell_scripts) + "\n")
            else:
                f.write(shell_scripts + "\n")
            
            f.write("\n--- Enlaces SimbÃ³licos Rotos ---\n")
            broken_symlinks = data.get("broken_symlinks", [])
            if isinstance(broken_symlinks, list):
                f.write("\n".join(broken_symlinks) + "\n")
            else:
                f.write(broken_symlinks + "\n")
            
            f.write("\n--- Configuraciones Sensibles en PHP ---\n")
            f.write(data.get("php_configs", "No se encontraron configuraciones sensibles en PHP.\n"))
            
            f.write("\n--- Respaldos ---\n")
            backups = data.get("backups", {})
            for key, value in backups.items():
                f.write(f"{key}:\n{value}\n")
        
        print(f"[+] Informe generado: {report_path}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
