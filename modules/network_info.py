import os
import subprocess
import socket

def list_network_interfaces():
    """Lista y analiza las interfaces de red del sistema."""
    try:
        result = subprocess.getoutput("ip link")
        return result
    except Exception as e:
        return f"Error al listar las interfaces: {str(e)}"

def analyze_hostname_and_dns():
    """Recopila informaciÃ³n del hostname, /etc/hosts y configuraciones DNS."""
    try:
        hostname = socket.gethostname()
        with open('/etc/hosts', 'r') as hosts_file:
            hosts_content = hosts_file.read()
        resolv_conf = subprocess.getoutput("cat /etc/resolv.conf")
        return {
            "Hostname": hostname,
            "/etc/hosts": hosts_content,
            "DNS Configurations": resolv_conf,
        }
    except Exception as e:
        return f"Error al analizar el hostname y DNS: {str(e)}"

def analyze_network_configuration():
    """Analiza la configuraciÃ³n de red y los vecinos en la red."""
    try:
        network_config = subprocess.getoutput("ip addr show")
        neighbors = subprocess.getoutput("ip neigh show")
        return {
            "Network Configuration": network_config,
            "Network Neighbors": neighbors,
        }
    except Exception as e:
        return f"Error al analizar la configuraciÃ³n de red: {str(e)}"

def list_active_ports():
    """Lista los puertos activos en estado de escucha."""
    try:
        listening_ports = subprocess.getoutput("ss -tuln")
        return listening_ports
    except Exception as e:
        return f"Error al listar los puertos activos: {str(e)}"

def check_tcpdump_permissions():
    """Verifica si se puede ejecutar tcpdump con los permisos actuales."""
    try:
        result = subprocess.run(['tcpdump', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return "tcpdump estÃ¡ instalado y accesible."
        else:
            return "tcpdump no estÃ¡ disponible o no tiene permisos suficientes."
    except FileNotFoundError:
        return "tcpdump no estÃ¡ instalado en este sistema."
    except Exception as e:
        return f"Error al verificar tcpdump: {str(e)}"

def create_report_directory():
    """Crea la carpeta 'report' si no existe."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Recoge toda la informaciÃ³n del mÃ³dulo y la devuelve como un diccionario."""
    return {
        "network_interfaces": list_network_interfaces(),
        "hostname_and_dns": analyze_hostname_and_dns(),
        "network_configuration": analyze_network_configuration(),
        "active_ports": list_active_ports(),
        "tcpdump_permissions": check_tcpdump_permissions(),
    }

def generate_report(data, output_file="network_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        # Crear el directorio report
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w") as f:
            f.write("=== Informe de InformaciÃ³n de Red ===\n")
            
            f.write("\n--- Interfaces de Red ---\n")
            f.write(data.get("network_interfaces", "No se pudo obtener informaciÃ³n.\n"))
            
            f.write("\n--- Hostname y ConfiguraciÃ³n de DNS ---\n")
            dns_info = data.get("hostname_and_dns", {})
            for key, value in dns_info.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- ConfiguraciÃ³n de Red ---\n")
            network_config = data.get("network_configuration", {})
            for key, value in network_config.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Puertos Activos ---\n")
            f.write(data.get("active_ports", "No se encontraron puertos activos.\n"))
            
            f.write("\n--- VerificaciÃ³n de tcpdump ---\n")
            f.write(data.get("tcpdump_permissions", "No se pudo verificar tcpdump.\n"))
        
        print(f"[+] Informe generado: {report_path}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
