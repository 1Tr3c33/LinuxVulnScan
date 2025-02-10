import subprocess


def find_useful_software():
    """Busca software útil instalado y ejecutable desde el terminal."""
    try:
        software = subprocess.getoutput("compgen -c | sort | uniq")
        return software.splitlines() if software else "No se encontraron programas disponibles en el terminal."
    except Exception as e:
        return f"Error al buscar software útil: {str(e)}"


def find_compilers_and_packages():
    """Busca compiladores instalados y paquetes vulnerables."""
    try:
        # Compiladores
        compilers = subprocess.getoutput("which gcc g++ clang make cmake 2>/dev/null")
        # Paquetes instalados mediante pkg o brew
        pkg_packages = subprocess.getoutput("pkg info 2>/dev/null || echo 'pkg no disponible'")
        brew_packages = subprocess.getoutput("brew list 2>/dev/null || echo 'brew no disponible'")
        # Paquetes vulnerables
        vulnerable_packages = subprocess.getoutput("dpkg -l | grep -i 'vulnerable' 2>/dev/null || echo 'No hay paquetes vulnerables.'")
        
        return {
            "Compilers": compilers if compilers else "No se encontraron compiladores instalados.",
            "Packages via pkg": pkg_packages,
            "Packages via brew": brew_packages,
            "Vulnerable Packages": vulnerable_packages,
        }
    except Exception as e:
        return f"Error al buscar compiladores y paquetes: {str(e)}"


def check_ctr_tool():
    """Verifica si la herramienta ctr de containerd está disponible."""
    try:
        result = subprocess.run(["ctr", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip() if result.returncode == 0 else "ctr no está disponible."
    except FileNotFoundError:
        return "ctr no está instalado en este sistema."
    except Exception as e:
        return f"Error al verificar ctr: {str(e)}"


def find_specific_programs():
    """Busca programas específicos y útiles instalados en el sistema."""
    programs = [
        "docker", "kcpassword", "phpsession", "apache2", "kerberos", "pam", "aws", "vault",
        "leak", "git", "postgresql", "dovecot", "log4shell", "rune", "freelpa", "mysql", "skey",
        "gitlab", "pgp", "screen", "splunk", "ssh", "tmux", "vault", "yubikey"
    ]
    found_programs = {}
    for program in programs:
        try:
            result = subprocess.run(["which", program], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            found_programs[program] = "Encontrado" if result.returncode == 0 else "No encontrado"
        except Exception as e:
            found_programs[program] = f"Error: {str(e)}"
    return found_programs


def generate_report(data, output_file="software_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Software del Sistema ===\n")
            
            f.write("\n--- Software Útil Instalado ---\n")
            software_list = data.get("useful_software", [])
            if isinstance(software_list, list):
                f.write("\n".join(software_list) + "\n")
            else:
                f.write(software_list + "\n")
            
            f.write("\n--- Compiladores y Paquetes ---\n")
            compilers_packages = data.get("compilers_packages", {})
            for key, value in compilers_packages.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Herramienta ctr ---\n")
            f.write(data.get("ctr_tool", "No se pudo verificar ctr.\n"))
            
            f.write("\n--- Programas Específicos ---\n")
            specific_programs = data.get("specific_programs", {})
            for program, status in specific_programs.items():
                f.write(f"{program}: {status}\n")
        
        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "useful_software": find_useful_software(),
        "compilers_packages": find_compilers_and_packages(),
        "ctr_tool": check_ctr_tool(),
        "specific_programs": find_specific_programs(),
    }
    generate_report(data)