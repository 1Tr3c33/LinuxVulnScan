import os
import platform
import subprocess
from datetime import datetime

def get_os_info():
    """Retrieves information about the operating system and kernel."""
    return {
        "OS": platform.system(),
        "Kernel Version": platform.release(),
        "Kernel Details": platform.version(),
        "Architecture": platform.architecture(),
        "Hostname": platform.node(),
    }

def check_sudo_version():
    """Checks if the sudo command is available and retrieves its version."""
    try:
        result = subprocess.run(['sudo', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.splitlines()[0] if result.returncode == 0 else "sudo is not available."
    except FileNotFoundError:
        return "sudo is not installed on this system."
    except Exception as e:
        return f"Error verifying sudo: {str(e)}"

def get_path_analysis():
    """Displays PATH directories and verifies its configuration."""
    paths = os.getenv("PATH", "").split(":")
    return {"PATH": paths, "Total Directories": len(paths)}

def get_time_and_date():
    """Retrieves the current system date and time."""
    now = datetime.now()
    return {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
    }

def create_report_directory():
    """Creates the 'report' folder if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    return {
        "os_info": get_os_info(),
        "sudo_version": check_sudo_version(),
        "path_analysis": get_path_analysis(),
        "time_and_date": get_time_and_date(),
    }

def generate_report(data, output_file="system_info_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== System Information Report ===\n")
            
            f.write("\n--- Operating System Information ---\n")
            os_info = data.get("os_info", {})
            for key, value in os_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Sudo Version ---\n")
            f.write(data.get("sudo_version", "Unable to verify sudo.\n"))
            
            f.write("\n--- PATH Analysis ---\n")
            path_analysis = data.get("path_analysis", {})
            for key, value in path_analysis.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n--- Date and Time ---\n")
            time_date = data.get("time_and_date", {})
            for key, value in time_date.items():
                f.write(f"{key}: {value}\n")
        
        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
