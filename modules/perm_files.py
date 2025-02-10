import os
import subprocess


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
    """Analiza archivos con Listas de Control de Acceso (ACLs) configuradas."""
    try:
        acl_files = subprocess.getoutput("getfacl -R / 2>/dev/null | grep 'file:'")
        return acl_files if acl_files else "No se encontraron archivos con ACLs configuradas."
    except Exception as e:
        return f"Error al analizar archivos con ACLs: {str(e)}"


def analyze_capabilities():
    """Analiza capacidades configuradas en el sistema para procesos y archivos."""
    try:
        capabilities = subprocess.getoutput("getcap -r / 2>/dev/null")
        return capabilities if capabilities else "No se encontraron capacidades configuradas."
    except Exception as e:
        return f"Error al analizar capacidades: {str(e)}"


def analyze_capability_conf():
    """Examina /etc/security/capability.conf para determinar asignaciones de capacidades."""
    try:
        if os.path.exists('/etc/security/capability.conf'):
            with open('/etc/security/capability.conf', 'r') as file:
                content = file.read()
            return content
        else:
            return "/etc/security/capability.conf no existe."
    except Exception as e:
        return f"Error al analizar capability.conf: {str(e)}"


def analyze_ld_so_config():
    """Verifica configuraciones relacionadas con ld.so en busca de vulnerabilidades."""
    try:
        ld_so_files = subprocess.getoutput("ls -l /etc/ld.so*")
        return ld_so_files if ld_so_files else "No se encontraron configuraciones ld.so."
    except Exception as e:
        return f"Error al analizar ld.so: {str(e)}"


def analyze_profile_d_scripts():
    """Identifica vulnerabilidades en archivos de configuración en /etc/profile.d/."""
    try:
        profile_files = subprocess.getoutput("ls -l /etc/profile.d/")
        return profile_files if profile_files else "No se encontraron scripts en /etc/profile.d/."
    except Exception as e:
        return f"Error al analizar scripts en /etc/profile.d/: {str(e)}"


def analyze_service_permissions():
    """Detecta configuraciones peligrosas en directorios relacionados con servicios del sistema."""
    try:
        risky_directories = subprocess.getoutput("find /etc/systemd/system /lib/systemd/system -type d -perm -o+w 2>/dev/null")
        return risky_directories if risky_directories else "No se encontraron directorios con permisos peligrosos."
    except Exception as e:
        return f"Error al analizar permisos de servicios: {str(e)}"


def analyze_apparmor_profiles():
    """Analiza los perfiles binarios de AppArmor configurados en el sistema."""
    try:
        if os.path.exists('/etc/apparmor.d'):
            profiles = subprocess.getoutput("ls -l /etc/apparmor.d/")
            return profiles if profiles else "No se encontraron perfiles de AppArmor configurados."
        else:
            return "AppArmor no está configurado en este sistema."
    except Exception as e:
        return f"Error al analizar perfiles de AppArmor: {str(e)}"


def generate_report(data, output_file="perm_files_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Archivos y Permisos ===\n")
            
            f.write("\n--- Archivos con SUID Habilitado ---\n")
            f.write(data.get("suid_files", "No se pudo obtener información.\n"))
            
            f.write("\n--- Archivos con SGID Habilitado ---\n")
            f.write(data.get("sgid_files", "No se pudo obtener información.\n"))
            
            f.write("\n--- Archivos con ACLs Configuradas ---\n")
            f.write(data.get("acl_files", "No se pudo obtener información.\n"))
            
            f.write("\n--- Capacidades Configuradas ---\n")
            f.write(data.get("capabilities", "No se pudo obtener información.\n"))
            
            f.write("\n--- Contenido de capability.conf ---\n")
            f.write(data.get("capability_conf", "No se pudo obtener información.\n"))
            
            f.write("\n--- Configuraciones ld.so ---\n")
            f.write(data.get("ld_so_config", "No se pudo obtener información.\n"))
            
            f.write("\n--- Archivos en /etc/profile.d/ ---\n")
            f.write(data.get("profile_d_scripts", "No se pudo obtener información.\n"))
            
            f.write("\n--- Permisos de Servicios ---\n")
            f.write(data.get("service_permissions", "No se pudo obtener información.\n"))
            
            f.write("\n--- Perfiles de AppArmor ---\n")
            f.write(data.get("apparmor_profiles", "No se pudo obtener información.\n"))
        
        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "suid_files": analyze_suid_files(),
        "sgid_files": analyze_sgid_files(),
        "acl_files": analyze_acl_files(),
        "capabilities": analyze_capabilities(),
        "capability_conf": analyze_capability_conf(),
        "ld_so_config": analyze_ld_so_config(),
        "profile_d_scripts": analyze_profile_d_scripts(),
        "service_permissions": analyze_service_permissions(),
        "apparmor_profiles": analyze_apparmor_profiles(),
    }
    generate_report(data)
