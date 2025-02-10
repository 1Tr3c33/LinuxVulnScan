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
    """Recopila información del hostname, /etc/hosts y configuraciones DNS."""
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
    """Analiza la configuración de red y los vecinos en la red."""
    try:
        network_config = subprocess.getoutput("ip addr show")
        neighbors = subprocess.getoutput("ip neigh show")
        return {
            "Network Configuration": network_config,
            "Network Neighbors": neighbors,
        }
    except Exception as e:
        return f"Error al analizar la configuración de red: {str(e)}"


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
            return "tcpdump está instalado y accesible."
        else:
            return "tcpdump no está disponible o no tiene permisos suficientes."
    except FileNotFoundError:
        return "tcpdump no está instalado en este sistema."
    except Exception as e:
        return f"Error al verificar tcpdump: {str(e)}"


def check_iptables_rules():
    """Verifica y muestra las reglas configuradas en iptables."""
    try:
        iptables_rules = subprocess.getoutput("iptables -L")
        return iptables_rules
    except Exception as e:
        return f"Error al mostrar las reglas de iptables: {str(e)}"


def show_inetd_and_xinetd():
    """Muestra el contenido de /etc/inetd.conf y /etc/xinetd.conf."""
    files = ['/etc/inetd.conf', '/etc/xinetd.conf']
    results = {}
    for file in files:
        try:
            with open(file, 'r') as f:
                results[file] = f.read()
        except FileNotFoundError:
            results[file] = f"{file} no existe."
        except Exception as e:
            results[file] = f"Error al leer {file}: {str(e)}"
    return results


def generate_report(data, output_file="network_info_report.txt"):
    """Genera un informe en texto plano con los resultados obtenidos."""
    try:
        with open(output_file, "w") as f:
            f.write("=== Informe de Información de Red ===\n")
            
            f.write("\n--- Interfaces de Red ---\n")
            f.write(data.get("network_interfaces", "No se pudo obtener información.\n"))
            
            f.write("\n--- Hostname y DNS ---\n")
            hostname_dns = data.get("hostname_dns", {})
            for key, value in hostname_dns.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Configuración de Red ---\n")
            network_config = data.get("network_config", {})
            for key, value in network_config.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Puertos Activos ---\n")
            f.write(data.get("active_ports", "No se pudo obtener información.\n"))
            
            f.write("\n--- Verificación de tcpdump ---\n")
            f.write(data.get("tcpdump_permissions", "No se pudo verificar tcpdump.\n"))
            
            f.write("\n--- Reglas de iptables ---\n")
            f.write(data.get("iptables_rules", "No se pudo obtener información sobre iptables.\n"))
            
            f.write("\n--- Archivos inetd y xinetd ---\n")
            inetd_xinetd = data.get("inetd_xinetd", {})
            for file, content in inetd_xinetd.items():
                f.write(f"\n{file}:\n{content}\n")
        
        print(f"[+] Informe generado: {output_file}")
    except Exception as e:
        print(f"[-] Error al generar el informe: {str(e)}")


if __name__ == "__main__":
    # Ejecutar todas las funciones y generar el informe
    data = {
        "network_interfaces": list_network_interfaces(),
        "hostname_dns": analyze_hostname_and_dns(),
        "network_config": analyze_network_configuration(),
        "active_ports": list_active_ports(),
        "tcpdump_permissions": check_tcpdump_permissions(),
        "iptables_rules": check_iptables_rules(),
        "inetd_xinetd": show_inetd_and_xinetd(),
    }
    generate_report(data)