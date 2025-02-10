import os
import subprocess
from pathlib import Path


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
    """Identifica enlaces simbólicos rotos en los directorios PATH."""
    try:
        paths = os.getenv("PATH", "").split(":")
        broken_symlinks = []
        for path in paths:
            broken_symlinks += subprocess.getoutput(f"find {path} -xtype l 2>/dev/null").splitlines()
        return broken_symlinks if broken_symlinks else "No se encontraron enlaces simbólicos rotos."
    except Exception as e:
        return f"Error al buscar enlaces simbólicos rotos: {str(e)}"


def find_executables_added_by_users():
    """Busca archivos ejecutables que podrían haber sido añadidos por usuarios en el sistema."""
    try:
        executables = subprocess.getoutput("find / -type f -perm -u+x 2>/dev/null")
        return executables if executables else "No se encontraron ejecutables añadidos por usuarios."
    except Exception as e:
        return f"Error al buscar ejecutables: {str(e)}"


def analyze_opt_directory():
    """Verifica si el directorio /opt contiene elementos."""
    try:
        contents = os.listdir('/opt')
        return contents if contents else "/opt está vacío."
    except FileNotFoundError:
        return "/opt no existe en este sistema."
    except Exception as e:
        return f"Error al analizar /opt: {str(e)}"


def find_unexpected_root_files():
    """Busca elementos inesperados en el directorio raíz."""
    try:
        common_dirs = set(["bin", "boot", "dev", "etc", "home", "lib", "opt", "proc", "root", "sbin", "tmp", "usr", "var"])
        root_contents = set(os.listdir('/'))
        unexpected = root_contents - common_dirs
        return unexpected if unexpected else "No se encontraron elementos inesperados en el directorio raíz."
    except Exception as e:
        return f"Error al analizar el directorio raíz: {str(e)}"


def writable_logs_and_logrotate():
    """Busca archivos de registro .log que sean escribibles y verifica logrotate."""
    try:
        writable_logs = subprocess.getoutput("find /var/log -type f -name '*.log' -writable 2>/dev/null")
        logrotate_version = subprocess.getoutput("logrotate --version 2>/dev/null")
        return {
            "Writable Logs": writable_logs if writable_logs else "No se encontraron logs escribibles.",
            "Logrotate Version": logrotate_version if logrotate_version else "logrotate no está instalado."
        }
    except Exception as e:
        return f"Error al analizar logs: {str(e)}"


def generate_report(data, output_file="interesting_files_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Archivos y Configuraciones Interesantes ===\n")
            
            f.write("\n--- Scripts .sh en PATH ---\n")
            f.write(data.get("shell_scripts", "No se pudo obtener información.\n"))
            
            f.write("\n--- Enlaces Simbólicos Rotos ---\n")
            f.write(data.get("broken_symlinks", "No se pudo obtener información.\n"))
            
            f.write("\n--- Ejecutables Añadidos por Usuarios ---\n")
            f.write(data.get("executables", "No se pudo obtener información.\n"))
            
            f.write("\n--- Contenido de /opt ---\n")
            f.write(data.get("opt_contents", "No se pudo obtener información.\n"))
            
            f.write("\n--- Elementos Inesperados en / ---\n")
            f.write(data.get("unexpected_root_files", "No se pudo obtener información.\n"))
            
            f.write("\n--- Logs Escribibles y logrotate ---\n")
            writable_logs = data.get("writable_logs", {})
            for key, value in writable_logs.items():
                f.write(f"{key}: {value}\n")
        
        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "shell_scripts": "\n".join(list_shell_scripts_in_path()),
        "broken_symlinks": "\n".join(find_broken_symlinks()),
        "executables": find_executables_added_by_users(),
        "opt_contents": analyze_opt_directory(),
        "unexpected_root_files": "\n".join(find_unexpected_root_files()),
        "writable_logs": writable_logs_and_logrotate(),
    }
    generate_report(data)