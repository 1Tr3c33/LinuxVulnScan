import os
import platform
import subprocess
from datetime import datetime


def get_os_info():
    """Recupera información del sistema operativo y del kernel."""
    return {
        "OS": platform.system(),
        "Kernel Version": platform.release(),
        "Kernel Details": platform.version(),
        "Architecture": platform.architecture(),
        "Hostname": platform.node(),
    }


def check_sudo_version():
    """Verifica si el comando sudo está presente y muestra su versión."""
    try:
        result = subprocess.run(['sudo', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.splitlines()[0] if result.returncode == 0 else "sudo no está disponible."
    except FileNotFoundError:
        return "sudo no está instalado en este sistema."
    except Exception as e:
        return f"Error al verificar sudo: {str(e)}"


def get_path_analysis():
    """Muestra las rutas del PATH y verifica su configuración."""
    paths = os.getenv("PATH", "").split(":")
    return {"PATH": paths, "Total Directories": len(paths)}


def get_time_and_date():
    """Muestra la hora y fecha actuales."""
    now = datetime.now()
    return {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
    }


def check_fstab():
    """Verifica /etc/fstab en busca de configuraciones de archivos no montados."""
    try:
        with open('/etc/fstab', 'r') as fstab:
            return fstab.readlines()
    except Exception as e:
        return f"Error al leer /etc/fstab: {str(e)}"


def check_disks_and_smb():
    """Comprueba discos y recursos SMB en /dev."""
    try:
        dev_files = os.listdir('/dev')
        smb_mounts = subprocess.getoutput("mount | grep -i 'type cifs'")
        return {
            "Disks": dev_files,
            "SMB Mounts": smb_mounts,
        }
    except Exception as e:
        return {"error": f"Error al analizar discos y SMB: {str(e)}"}


def analyze_environment_variables():
    """Examina variables de entorno en busca de información sensible."""
    env_vars = os.environ
    sensitive_data = {key: value for key, value in env_vars.items() if any(keyword in key.lower() for keyword in ['password', 'key', 'secret'])}
    return sensitive_data


def check_exploit_suggestions():
    """Ejecuta Linux Exploit Suggester."""
    try:
        result = subprocess.getoutput("linux-exploit-suggester")
        return result if result else "Linux Exploit Suggester no detectó vulnerabilidades."
    except Exception as e:
        return f"Error ejecutando Linux Exploit Suggester: {str(e)}"


def check_polkit_vulnerability():
    """Comprueba si el sistema es vulnerable a Polkit (CVE-2021-3560)."""
    try:
        result = subprocess.getoutput("pkexec --version")
        return result if "pkexec" in result else "Polkit no está presente o no es vulnerable."
    except Exception as e:
        return f"Error al verificar Polkit: {str(e)}"


def audit_security_configurations():
    """Audita configuraciones de seguridad importantes en el sistema."""
    try:
        return {
            "ASLR (Address Space Layout Randomization)": subprocess.getoutput("cat /proc/sys/kernel/randomize_va_space"),
            "SELinux Status": subprocess.getoutput("getenforce") if os.path.exists("/usr/sbin/getenforce") else "No instalado",
            "AppArmor Status": subprocess.getoutput("aa-status") if os.path.exists("/usr/sbin/aa-status") else "No instalado",
        }
    except Exception as e:
        return {"error": f"Error al auditar configuraciones de seguridad: {str(e)}"}


def generate_report(data, output_file="system_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Información del Sistema ===\n")
            
            f.write("\n--- Información del Sistema Operativo ---\n")
            os_info = data.get("os_info", {})
            for key, value in os_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Versión de sudo ---\n")
            f.write(data.get("sudo_version", "No se pudo verificar sudo.\n"))
            
            f.write("\n--- Análisis de PATH ---\n")
            path_analysis = data.get("path_analysis", {})
            for key, value in path_analysis.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Hora y Fecha ---\n")
            time_date = data.get("time_and_date", {})
            for key, value in time_date.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Verificación de /etc/fstab ---\n")
            fstab = data.get("fstab", "No se pudo obtener información.\n")
            if isinstance(fstab, list):
                f.write("".join(fstab))
            else:
                f.write(fstab + "\n")
            
            f.write("\n--- Discos y SMB Mounts ---\n")
            disks_smb = data.get("disks_and_smb", {})
            for key, value in disks_smb.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Variables de Entorno Sensibles ---\n")
            env_vars = data.get("environment_variables", {})
            for key, value in env_vars.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Sugerencias de Exploits ---\n")
            f.write(data.get("exploit_suggestions", "No se pudo obtener información.\n"))
            
            f.write("\n--- Vulnerabilidad Polkit ---\n")
            f.write(data.get("polkit_vulnerability", "No se pudo verificar Polkit.\n"))
            
            f.write("\n--- Auditoría de Configuraciones de Seguridad ---\n")
            security_audit = data.get("security_audit", {})
            for key, value in security_audit.items():
                f.write(f"{key}: {value}\n")
        
        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "os_info": get_os_info(),
        "sudo_version": check_sudo_version(),
        "path_analysis": get_path_analysis(),
        "time_and_date": get_time_and_date(),
        "fstab": check_fstab(),
        "disks_and_smb": check_disks_and_smb(),
        "environment_variables": analyze_environment_variables(),
        "exploit_suggestions": check_exploit_suggestions(),
        "polkit_vulnerability": check_polkit_vulnerability(),
        "security_audit": audit_security_configurations(),
    }
    generate_report(data)