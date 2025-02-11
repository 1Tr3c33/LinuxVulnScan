import os
import subprocess

def check_container_tools():
    """Comprueba si herramientas relacionadas con contenedores están instaladas en el sistema."""
    tools = ["docker", "podman", "kubectl", "containerd", "runc", "amicontained"]
    installed_tools = {}
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            installed_tools[tool] = result.stdout.strip() if result.returncode == 0 else "No disponible"
        except FileNotFoundError:
            installed_tools[tool] = "No instalado"
    return installed_tools

def check_kubernetes_tokens():
    """Busca tokens montados en volÃºmenes tmpfs asociados con Kubernetes."""
    try:
        tokens = subprocess.getoutput("find /var/run/secrets/kubernetes.io/ -type f 2>/dev/null")
        return tokens if tokens else "No se encontraron tokens de Kubernetes montados."
    except Exception as e:
        return f"Error al buscar tokens de Kubernetes: {str(e)}"

def verify_containers():
    """Verifica si el entorno actual es un contenedor y detecta contenedores en ejecuciÃ³n."""
    try:
        # Comprueba si el sistema estÃ¡ dentro de un contenedor
        is_container = os.path.exists('/.dockerenv') or "container" in subprocess.getoutput("cat /proc/1/cgroup")
        
        # Detecta contenedores en ejecuciÃ³n
        docker_containers = subprocess.getoutput("docker ps --format '{{.ID}}: {{.Image}} ({{.Status}})'") if os.system("which docker > /dev/null 2>&1") == 0 else "Docker no instalado."
        podman_containers = subprocess.getoutput("podman ps --format '{{.ID}}: {{.Image}} ({{.Status}})'") if os.system("which podman > /dev/null 2>&1") == 0 else "Podman no instalado."
        
        return {
            "Is Container": is_container,
            "Docker Containers": docker_containers,
            "Podman Containers": podman_containers,
        }
    except Exception as e:
        return f"Error al verificar contenedores: {str(e)}"

def analyze_docker_group():
    """Proporciona informaciÃ³n sobre el grupo de Docker y configuraciones relacionadas."""
    try:
        group_members = subprocess.getoutput("getent group docker")
        rootless_support = subprocess.getoutput("docker info --format '{{.Rootless}}'") if os.system("which docker > /dev/null 2>&1") == 0 else "No disponible"
        overlays = subprocess.getoutput("docker info --format '{{.Driver}}'") if os.system("which docker > /dev/null 2>&1") == 0 else "No disponible"
        
        return {
            "Docker Group Members": group_members if group_members else "No se encontrÃ³ el grupo docker.",
            "Docker Rootless Support": rootless_support,
            "Docker Overlay/Storage Driver": overlays,
        }
    except Exception as e:
        return f"Error al analizar configuraciones de Docker: {str(e)}"

def create_report_directory():
    """Crea la carpeta 'report' si no existe."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Recoge toda la informaciÃ³n del mÃ³dulo y la devuelve como un diccionario."""
    return {
        "container_tools": check_container_tools(),
        "kubernetes_tokens": check_kubernetes_tokens(),
        "containers_status": verify_containers(),
        "docker_group_info": analyze_docker_group(),
    }

def generate_report(data, output_file="container_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        # Crear el directorio report
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Informe de InformaciÃ³n de Contenedores ===\n")
            
            f.write("\n--- Herramientas de Contenedores Instaladas ---\n")
            container_tools = data.get("container_tools", {})
            for tool, status in container_tools.items():
                f.write(f"{tool}: {status}\n")
            
            f.write("\n--- Tokens de Kubernetes ---\n")
            f.write(data.get("kubernetes_tokens", "No se encontraron tokens de Kubernetes.\n"))
            
            f.write("\n--- VerificaciÃ³n de Contenedores ---\n")
            containers_status = data.get("containers_status", {})
            for key, value in containers_status.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- InformaciÃ³n del Grupo Docker ---\n")
            docker_group_info = data.get("docker_group_info", {})
            for key, value in docker_group_info.items():
                f.write(f"{key}: {value}\n")
        
        print(f"[+] Informe generado: {report_path}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
