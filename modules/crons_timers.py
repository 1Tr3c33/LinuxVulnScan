import os
import subprocess

def analyze_running_processes():
    """Analyzes running processes and the user executing them."""
    try:
        processes = subprocess.getoutput("ps aux")
        return processes
    except Exception as e:
        return f"Error analyzing running processes: {str(e)}"

def search_credential_processes():
    """Searches for processes that might store credentials in memory."""
    try:
        suspicious_processes = subprocess.getoutput("ps aux | grep -i 'ssh\\|login\\|passwd\\|gpg\\|vault'")
        return suspicious_processes if suspicious_processes else "No suspicious processes found."
    except Exception as e:
        return f"Error searching for processes that might store credentials: {str(e)}"

def analyze_cron_jobs():
    """Analyzes scheduled tasks in cron, anacron, incron, and at."""
    try:
        cron_jobs = subprocess.getoutput("cat /etc/crontab; crontab -l 2>/dev/null; ls /etc/cron.d")
        anacron_jobs = subprocess.getoutput("ls /etc/anacrontab")
        incron_jobs = subprocess.getoutput("incrontab -l 2>/dev/null")
        at_jobs = subprocess.getoutput("atq")
        return {
            "Cron Jobs": cron_jobs,
            "Anacron Jobs": anacron_jobs,
            "Incron Jobs": incron_jobs,
            "At Jobs": at_jobs,
        }
    except Exception as e:
        return f"Error analyzing scheduled tasks: {str(e)}"

def analyze_systemd_timers():
    """Analyzes timers configured in the system through systemd."""
    try:
        timers = subprocess.getoutput("systemctl list-timers --all")
        return timers if timers else "No timers configured."
    except Exception as e:
        return f"Error analyzing systemd timers: {str(e)}"

def create_report_directory():
    """Creates the 'report' directory if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    return {
        "running_processes": analyze_running_processes(),
        "suspicious_processes": search_credential_processes(),
        "cron_jobs": analyze_cron_jobs(),
        "systemd_timers": analyze_systemd_timers(),
    }

def generate_report(data, output_file="crons_timers_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Cron Jobs and Timers Report ===\n")
            
            f.write("\n--- Running Processes ---\n")
            f.write(data.get("running_processes", "Could not retrieve process information.\n"))
            
            f.write("\n--- Processes that Might Store Credentials ---\n")
            f.write(data.get("suspicious_processes", "No suspicious processes found.\n"))
            
            f.write("\n--- Scheduled Tasks ---\n")
            cron_jobs = data.get("cron_jobs", {})
            for key, value in cron_jobs.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- System Timers ---\n")
            f.write(data.get("systemd_timers", "No timers configured.\n"))
        
        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)
