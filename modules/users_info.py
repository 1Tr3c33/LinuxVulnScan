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
    """Analiza los procesos en ejecución en el sistema."""
    try:
        processes = subprocess.getoutput("ps aux")
        return processes
    except Exception as e:
        return f"Error al analizar procesos: {str(e)}"


def brute_su_check():
    """Realiza una prueba básica para detectar si el comando su puede ser explotado."""
    try:
        result = subprocess.run(['su', '-c', 'echo Test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "El comando 'su' puede ser utilizado." if result.returncode == 0 else f"No se puede usar 'su': {result.stderr.strip()}"
    except Exception as e:
        return f"Error al verificar 'su': {str(e)}"


def analyze_sudo_configuration():
    """Analiza la configuración de sudo en el sistema."""
    try:
        sudoers_content = subprocess.getoutput("cat /etc/sudoers")
        sudoers_d = subprocess.getoutput("ls -l /etc/sudoers.d")
        return {
            "/etc/sudoers": sudoers_content,
            "/etc/sudoers.d": sudoers_d,
        }
    except Exception as e:
        return {"error": f"Error al analizar la configuración de sudo: {str(e)}"}


def analyze_user_access():
    """Analiza qué usuarios tienen acceso al sistema."""
    try:
        active_users = subprocess.getoutput("who")
        return active_users.splitlines()
    except Exception as e:
        return {"error": f"Error al analizar los accesos de usuarios: {str(e)}"}


def check_last_logins():
    """Comprueba los últimos accesos al sistema."""
    try:
        last_accesses = subprocess.getoutput("last")
        return last_accesses.splitlines()
    except Exception as e:
        return {"error": f"Error al comprobar últimos accesos: {str(e)}"}


def password_policy_check():
    """Verifica la política de contraseñas y configuraciones relevantes."""
    try:
        policy = subprocess.getoutput("cat /etc/login.defs")
        return policy
    except Exception as e:
        return f"Error al verificar la política de contraseñas: {str(e)}"


def highlight_shell_users():
    """Destaca usuarios con shells válidas en /etc/passwd."""
    try:
        users_with_shells = []
        with open('/etc/passwd', 'r') as passwd_file:
            lines = passwd_file.readlines()
            for line in lines:
                parts = line.split(":")
                if parts[-1].strip() not in ['nologin', 'false']:
                    users_with_shells.append({
                        "User": parts[0],
                        "Shell": parts[-1].strip(),
                    })
        return users_with_shells
    except Exception as e:
        return {"error": f"Error al analizar shells en /etc/passwd: {str(e)}"}


def generate_report(data, output_file="users_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Información de Usuarios ===\n")
            
            f.write("\n--- Usuarios y Grupos ---\n")
            users_groups = data.get("users_and_groups", {})
            f.write("Usuarios:\n" + "\n".join(users_groups.get("Users", [])) + "\n")
            f.write("Grupos:\n" + "\n".join(users_groups.get("Groups", [])) + "\n")
            
            f.write("\n--- Procesos en Ejecución ---\n")
            f.write(data.get("running_processes", "No se pudo obtener información.\n"))
            
            f.write("\n--- Verificación de su ---\n")
            f.write(data.get("su_check", "No se pudo verificar 'su'.\n"))
            
            f.write("\n--- Configuración de sudo ---\n")
            sudo_config = data.get("sudo_configuration", {})
            for key, value in sudo_config.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Usuarios Activos ---\n")
            f.write("\n".join(data.get("user_access", [])) + "\n")
            
            f.write("\n--- Últimos Accesos ---\n")
            f.write("\n".join(data.get("last_logins", [])) + "\n")
            
            f.write("\n--- Políticas de Contraseñas ---\n")
            f.write(data.get("password_policy", "No se pudo obtener información.\n"))
            
            f.write("\n--- Usuarios con Shells ---\n")
            shell_users = data.get("shell_users", [])
            for user in shell_users:
                f.write(f"Usuario: {user['User']}, Shell: {user['Shell']}\n")
        
        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "users_and_groups": list_users_and_groups(),
        "running_processes": analyze_running_processes(),
        "su_check": brute_su_check(),
        "sudo_configuration": analyze_sudo_configuration(),
        "user_access": analyze_user_access(),
        "last_logins": check_last_logins(),
        "password_policy": password_policy_check(),
        "shell_users": highlight_shell_users(),
    }
    generate_report(data)