import os
import subprocess
import socket

def list_network_interfaces():
    """Lists and analyzes the network interfaces of the system."""
    try:
        result = subprocess.getoutput("ip link")
        return result
    except Exception as e:
        return f"Error listing network interfaces: {str(e)}"

def analyze_hostname_and_dns():
    """Collects information about the hostname, /etc/hosts, and DNS configurations."""
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
        return f"Error analyzing hostname and DNS: {str(e)}"

def analyze_network_configuration():
    """Analyzes the network configuration and neighbors on the network."""
    try:
        network_config = subprocess.getoutput("ip addr show")
        neighbors = subprocess.getoutput("ip neigh show")
        return {
            "Network Configuration": network_config,
            "Network Neighbors": neighbors,
        }
    except Exception as e:
        return f"Error analyzing network configuration: {str(e)}"

def list_active_ports():
    """Lists active ports in listening state."""
    try:
        listening_ports = subprocess.getoutput("ss -tuln")
        return listening_ports
    except Exception as e:
        return f"Error listing active ports: {str(e)}"

def check_tcpdump_permissions():
    """Checks if tcpdump can be executed with the current permissions."""
    try:
        result = subprocess.run(['tcpdump', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return "tcpdump is installed and accessible."
        else:
            return "tcpdump is not available or lacks sufficient permissions."
    except FileNotFoundError:
        return "tcpdump is not installed on this system."
    except Exception as e:
        return f"Error verifying tcpdump: {str(e)}"

def create_report_directory():
    """Creates the 'report' directory if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    return {
        "network_interfaces": list_network_interfaces(),
        "hostname_and_dns": analyze_hostname_and_dns(),
        "network_configuration": analyze_network_configuration(),
        "active_ports": list_active_ports(),
        "tcpdump_permissions": check_tcpdump_permissions(),
    }

def generate_report(data, output_file="network_info_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Network Information Report ===\n")
            
            f.write("\n--- Network Interfaces ---\n")
            f.write(data.get("network_interfaces", "Could not retrieve information.\n"))
            
            f.write("\n--- Hostname and DNS Configuration ---\n")
            dns_info = data.get("hostname_and_dns", {})
            for key, value in dns_info.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Network Configuration ---\n")
            network_config = data.get("network_configuration", {})
            for key, value in network_config.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Active Ports ---\n")
            f.write(data.get("active_ports", "No active ports found.\n"))
            
            f.write("\n--- tcpdump Verification ---\n")
            f.write(data.get("tcpdump_permissions", "Could not verify tcpdump.\n"))
        
        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
