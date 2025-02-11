import subprocess
import os

def analyze_suid_files():
    """Analyzes files with the SUID bit enabled."""
    try:
        suid_files = subprocess.getoutput("find / -perm -4000 -type f 2>/dev/null")
        return suid_files if suid_files else "No files with SUID enabled were found."
    except Exception as e:
        return f"Error analyzing SUID files: {str(e)}"

def analyze_sgid_files():
    """Analyzes files with the SGID bit enabled."""
    try:
        sgid_files = subprocess.getoutput("find / -perm -2000 -type f 2>/dev/null")
        return sgid_files if sgid_files else "No files with SGID enabled were found."
    except Exception as e:
        return f"Error analyzing SGID files: {str(e)}"

def analyze_acl_files():
    """Analyzes files with ACLs configured and selects the most relevant ones."""
    try:
        command = ("getfacl -R / 2>/dev/null | grep 'file:' | "
                   "grep -E '/etc|/home|/var|/usr' | sort -u")
        acl_files = subprocess.getoutput(command)
        filtered_files = "\n".join(acl_files.splitlines()[:100])  # Limit to 100 results
        return filtered_files if filtered_files else "No key files with ACLs configured were found."
    except Exception as e:
        return f"Error analyzing files with ACLs: {str(e)}"

def analyze_capabilities():
    """Analyzes system-configured capabilities for processes and files."""
    try:
        capabilities = subprocess.getoutput("getcap -r / 2>/dev/null")
        return capabilities if capabilities else "No configured capabilities were found."
    except Exception as e:
        return f"Error analyzing capabilities: {str(e)}"

def analyze_service_permissions():
    """Detects dangerous configurations in directories related to system services."""
    try:
        risky_directories = subprocess.getoutput("find /etc/systemd/system /lib/systemd/system -type d -perm -o+w 2>/dev/null")
        return risky_directories if risky_directories else "No directories with dangerous permissions were found."
    except Exception as e:
        return f"Error analyzing service permissions: {str(e)}"

def create_report_directory():
    """Creates the 'report' folder if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it in a dictionary."""
    return {
        "suid_files": analyze_suid_files(),
        "sgid_files": analyze_sgid_files(),
        "acl_files": analyze_acl_files(),
        "capabilities": analyze_capabilities(),
        "risky_service_permissions": analyze_service_permissions(),
    }

def generate_report(data, output_file="perm_files_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== File Permissions Report ===\n")
            
            f.write("\n--- Files with SUID ---\n")
            f.write(data.get("suid_files", "No files with SUID enabled were found.\n"))
            
            f.write("\n--- Files with SGID ---\n")
            f.write(data.get("sgid_files", "No files with SGID enabled were found.\n"))
            
            f.write("\n--- Key Files with ACLs Configured ---\n")
            f.write(data.get("acl_files", "No key files with ACLs configured were found.\n"))
            
            f.write("\n--- Configured Capabilities ---\n")
            f.write(data.get("capabilities", "No configured capabilities were found.\n"))
            
            f.write("\n--- Dangerous Permissions in Services ---\n")
            f.write(data.get("risky_service_permissions", "No directories with dangerous permissions were found.\n"))

        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)

