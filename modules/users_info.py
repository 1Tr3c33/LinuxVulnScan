import os
import subprocess

def list_users_and_groups():
    """Lists and categorizes all system users and groups."""
    try:
        users = subprocess.getoutput("cut -d: -f1 /etc/passwd")
        groups = subprocess.getoutput("cut -d: -f1 /etc/group")
        return {
            "Users": users.splitlines(),
            "Groups": groups.splitlines(),
        }
    except Exception as e:
        return {"error": f"Error listing users and groups: {str(e)}"}

def analyze_running_processes():
    """Analyzes running processes in the system."""
    try:
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return "Failed to list processes. Root privileges may be required."
        return result.stdout
    except Exception as e:
        return f"Error analyzing processes: {str(e)}"

def brute_su_check():
    """Checks if the 'su' command can be exploited."""
    try:
        if os.geteuid() != 0:
            return "'su' command cannot be verified without root privileges."
        
        result = subprocess.run(['su', '-c', 'echo Test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "'su' command can be used." if result.returncode == 0 else f"Cannot use 'su': {result.stderr.strip()}"
    except Exception as e:
        return f"Error verifying 'su': {str(e)}"

def analyze_user_access():
    """Analyzes which users have system access."""
    try:
        active_users = subprocess.getoutput("who")
        return active_users.splitlines()
    except Exception as e:
        return {"error": f"Error analyzing user access: {str(e)}"}

def check_last_logins():
    """Checks the system's last login records."""
    try:
        result = subprocess.run(["last"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return "Could not access login history. Root privileges may be required."
        return result.stdout.splitlines()
    except Exception as e:
        return f"Error checking last logins: {str(e)}"

def create_report_directory():
    """Creates the 'report' folder if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    return {
        "users_and_groups": list_users_and_groups(),
        "running_processes": analyze_running_processes(),
        "su_check": brute_su_check(),
        "user_access": analyze_user_access(),
        "last_logins": check_last_logins(),
    }

def generate_report(data, output_file="users_info_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== User Information Report ===\n")
            
            f.write("\n--- Users and Groups ---\n")
            users_groups = data.get("users_and_groups", {})
            for key, value in users_groups.items():
                f.write(f"{key}:\n" + "\n".join(value) + "\n")
            
            f.write("\n--- Running Processes ---\n")
            f.write(data.get("running_processes", "Failed to retrieve process information.\n"))
            
            f.write("\n--- 'su' Command Check ---\n")
            f.write(data.get("su_check", "Could not verify 'su' command.\n"))
            
            f.write("\n--- Active Users ---\n")
            active_users = data.get("user_access", [])
            if isinstance(active_users, list):
                f.write("\n".join(active_users) + "\n")
            else:
                f.write(active_users + "\n")
            
            f.write("\n--- Last Logins ---\n")
            last_logins = data.get("last_logins", [])
            if isinstance(last_logins, list):
                f.write("\n".join(last_logins) + "\n")
            else:
                f.write(last_logins + "\n")
        
        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

def check_root_privileges():
    """Checks if the program is running with root privileges."""
    if os.geteuid() != 0:
        print("[-] Warning: Some analyses may require root privileges for full results.")

if __name__ == "__main__":
    check_root_privileges()  # Check privileges before execution
    data = gather_data()
    generate_report(data)
