import os
import subprocess

def check_container_tools():
    """Checks if container-related tools are installed on the system."""
    tools = ["docker", "podman", "kubectl", "containerd", "runc", "amicontained"]
    installed_tools = {}
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            installed_tools[tool] = result.stdout.strip() if result.returncode == 0 else "Not available"
        except FileNotFoundError:
            installed_tools[tool] = "Not installed"
    return installed_tools

def check_kubernetes_tokens():
    """Searches for tokens mounted in tmpfs volumes related to Kubernetes."""
    try:
        tokens = subprocess.getoutput("find /var/run/secrets/kubernetes.io/ -type f 2>/dev/null")
        return tokens if tokens else "No Kubernetes tokens found."
    except Exception as e:
        return f"Error searching for Kubernetes tokens: {str(e)}"

def verify_containers():
    """Checks if the current environment is a container and detects running containers."""
    try:
        # Checks if the system is running inside a container
        is_container = os.path.exists('/.dockerenv') or "container" in subprocess.getoutput("cat /proc/1/cgroup")
        
        # Detects running containers
        docker_containers = subprocess.getoutput("docker ps --format '{{.ID}}: {{.Image}} ({{.Status}})'") if os.system("which docker > /dev/null 2>&1") == 0 else "Docker not installed."
        podman_containers = subprocess.getoutput("podman ps --format '{{.ID}}: {{.Image}} ({{.Status}})'") if os.system("which podman > /dev/null 2>&1") == 0 else "Podman not installed."
        
        return {
            "Is Container": is_container,
            "Docker Containers": docker_containers,
            "Podman Containers": podman_containers,
        }
    except Exception as e:
        return f"Error verifying containers: {str(e)}"

def analyze_docker_group():
    """Provides information about the Docker group and related configurations."""
    try:
        group_members = subprocess.getoutput("getent group docker")
        rootless_support = subprocess.getoutput("docker info --format '{{.Rootless}}'") if os.system("which docker > /dev/null 2>&1") == 0 else "Not available"
        overlays = subprocess.getoutput("docker info --format '{{.Driver}}'") if os.system("which docker > /dev/null 2>&1") == 0 else "Not available"
        
        return {
            "Docker Group Members": group_members if group_members else "Docker group not found.",
            "Docker Rootless Support": rootless_support,
            "Docker Overlay/Storage Driver": overlays,
        }
    except Exception as e:
        return f"Error analyzing Docker configurations: {str(e)}"

def create_report_directory():
    """Creates the 'report' directory if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    return {
        "container_tools": check_container_tools(),
        "kubernetes_tokens": check_kubernetes_tokens(),
        "containers_status": verify_containers(),
        "docker_group_info": analyze_docker_group(),
    }

def generate_report(data, output_file="container_info_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Container Information Report ===\n")
            
            f.write("\n--- Installed Container Tools ---\n")
            container_tools = data.get("container_tools", {})
            for tool, status in container_tools.items():
                f.write(f"{tool}: {status}\n")
            
            f.write("\n--- Kubernetes Tokens ---\n")
            f.write(data.get("kubernetes_tokens", "No Kubernetes tokens found.\n"))
            
            f.write("\n--- Container Verification ---\n")
            containers_status = data.get("containers_status", {})
            for key, value in containers_status.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Docker Group Information ---\n")
            docker_group_info = data.get("docker_group_info", {})
            for key, value in docker_group_info.items():
                f.write(f"{key}: {value}\n")
        
        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)

