import os
import subprocess
import shutil


def check_container_tools():
    """Comprueba si herramientas relacionadas con contenedores están instaladas en el sistema."""
    tools = ["docker", "podman", "kubectl", "containerd", "runc", "amicontained"]
    installed_tools = {}
    for tool in tools:
        if shutil.which(tool):
            try:
                result = subprocess.run([tool, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                installed_tools[tool] = result.stdout.strip() if result.returncode == 0 else "Error al ejecutar"
            except Exception as e:
                installed_tools[tool] = f"Error: {str(e)}"
        else:
            installed_tools[tool] = "No instalado"
    return installed_tools


def check_kubernetes_tokens():
    """Busca tokens montados en volúmenes tmpfs asociados con Kubernetes."""
    try:
        tokens = subprocess.getoutput("find /var/run/secrets/kubernetes.io/ -type f 2>/dev/null")
        return {"tokens_found": tokens.splitlines()} if tokens else {"tokens_found": [], "message": "No se encontraron tokens."}
    except Exception as e:
        return {"error": f"Error al buscar tokens: {str(e)}"}


def verify_containers():
    """Verifica si el entorno actual es un contenedor y detecta contenedores en ejecución."""
    try:
        is_container = os.path.exists('/.dockerenv') or "container" in subprocess.getoutput("cat /proc/1/cgroup")
        docker_containers = (
            subprocess.getoutput("docker ps --format '{{.ID}}: {{.Image}} ({{.Status}})'")
            if shutil.which("docker") else "Docker no instalado."
        )
        podman_containers = (
            subprocess.getoutput("podman ps --format '{{.ID}}: {{.Image}} ({{.Status}})'")
            if shutil.which("podman") else "Podman no instalado."
        )
        return {
            "is_container": is_container,
            "docker_containers": docker_containers,
            "podman_containers": podman_containers,
        }
    except Exception as e:
        return {"error": f"Error al verificar contenedores: {str(e)}"}


def analyze_docker_group():
    """Proporciona información sobre el grupo de Docker y configuraciones relacionadas."""
    try:
        group_members = subprocess.getoutput("getent group docker")
        rootless_support = (
            subprocess.getoutput("docker info --format '{{.Rootless}}'")
            if shutil.which("docker") else "No disponible"
        )
        overlays = (
            subprocess.getoutput("docker info --format '{{.Driver}}'")
            if shutil.which("docker") else "No disponible"
        )
        return {
            "docker_group_members": group_members if group_members else "No se encontró el grupo docker.",
            "docker_rootless_support": rootless_support,
            "docker_storage_driver": overlays,
        }
    except Exception as e:
        return {"error": f"Error al analizar configuraciones de Docker: {str(e)}"}


def audit_container_security():
    """Audita contenedores en busca de configuraciones inseguras y vulnerabilidades."""
    try:
        if shutil.which("docker"):
            result = subprocess.getoutput("docker scan --accept-license || echo 'Docker Scan no está disponible.'")
            return {"audit_result": result}
        return {"message": "Docker no instalado. Auditoría no disponible."}
    except Exception as e:
        return {"error": f"Error al realizar auditoría de seguridad: {str(e)}"}


def verify_with_amicontained():
    """Verifica el sistema en un contenedor utilizando amicontained."""
    try:
        if shutil.which("amicontained"):
            result = subprocess.getoutput("amicontained")
            return {"amicontained_output": result}
        return {"message": "amicontained no instalado."}
    except Exception as e:
        return {"error": f"Error al verificar con amicontained: {str(e)}"}


def generate_report(data, output_file="container_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Análisis de Contenedores ===\n")
            f.write("\n--- Herramientas de Contenedores Instaladas ---\n")
            for tool, status in data.get("container_tools", {}).items():
                f.write(f"{tool}: {status}\n")
            
            f.write("\n--- Tokens de Kubernetes ---\n")
            if data.get("kubernetes_tokens", {}).get("tokens_found"):
                for token in data["kubernetes_tokens"]["tokens_found"]:
                    f.write(f"Token: {token}\n")
            else:
                f.write(data["kubernetes_tokens"].get("message", "Error al buscar tokens.\n"))
            
            f.write("\n--- Verificación de Contenedores ---\n")
            f.write(f"¿Dentro de un contenedor?: {data['verify_containers'].get('is_container', 'Desconocido')}\n")
            f.write(f"Contenedores Docker:\n{data['verify_containers'].get('docker_containers', '')}\n")
            f.write(f"Contenedores Podman:\n{data['verify_containers'].get('podman_containers', '')}\n")
            
            f.write("\n--- Información del Grupo Docker ---\n")
            for key, value in data["analyze_docker_group"].items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Auditoría de Seguridad ---\n")
            f.write(f"{data['audit_container_security'].get('audit_result', '')}\n")
            
            f.write("\n--- Verificación con amicontained ---\n")
            f.write(data["verify_with_amicontained"].get("amicontained_output", "No disponible") + "\n")
        
        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "container_tools": check_container_tools(),
        "kubernetes_tokens": check_kubernetes_tokens(),
        "verify_containers": verify_containers(),
        "analyze_docker_group": analyze_docker_group(),
        "audit_container_security": audit_container_security(),
        "verify_with_amicontained": verify_with_amicontained(),
    }
    generate_report(data)