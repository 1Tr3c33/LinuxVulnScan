import os
import subprocess

def list_shell_scripts_in_path():
    """Lists .sh files in directories defined in the PATH variable."""
    try:
        paths = os.getenv("PATH", "").split(":")
        shell_scripts = []
        for path in paths:
            shell_scripts += subprocess.getoutput(f"find {path} -name '*.sh' 2>/dev/null").splitlines()
        return shell_scripts if shell_scripts else "No .sh scripts found in PATH directories."
    except Exception as e:
        return f"Error searching for .sh scripts: {str(e)}"

def find_broken_symlinks():
    """Identifies broken symbolic links in PATH directories."""
    try:
        paths = os.getenv("PATH", "").split(":")
        broken_symlinks = []
        for path in paths:
            broken_symlinks += subprocess.getoutput(f"find {path} -xtype l 2>/dev/null").splitlines()
        return broken_symlinks if broken_symlinks else "No broken symbolic links found."
    except Exception as e:
        return f"Error searching for broken symbolic links: {str(e)}"

def find_sensitive_php_configs():
    """Searches for passwords or sensitive configurations in PHP files."""
    try:
        php_files = subprocess.getoutput("grep -iR 'password\\|db_' /var/www 2>/dev/null")
        return php_files if php_files else "No sensitive configurations found in PHP files."
    except Exception as e:
        return f"Error analyzing PHP files: {str(e)}"

def find_backup_directories_and_files():
    """Searches for backup directories and files."""
    try:
        backup_dirs = subprocess.getoutput("find / -type d -name '*backup*' 2>/dev/null")
        backup_files = subprocess.getoutput("find / -type f -name '*.bak' -o -name '*.backup' 2>/dev/null")
        return {
            "Backup Directories": backup_dirs if backup_dirs else "No backup directories found.",
            "Backup Files": backup_files if backup_files else "No backup files found.",
        }
    except Exception as e:
        return f"Error searching for backups: {str(e)}"

def create_report_directory():
    """Creates the 'report' directory if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    return {
        "shell_scripts": list_shell_scripts_in_path(),
        "broken_symlinks": find_broken_symlinks(),
        "php_configs": find_sensitive_php_configs(),
        "backups": find_backup_directories_and_files(),
    }

def generate_report(data, output_file="interesting_files_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Interesting Files Report ===\n")
            
            f.write("\n--- .sh Scripts in PATH ---\n")
            shell_scripts = data.get("shell_scripts", [])
            if isinstance(shell_scripts, list):
                f.write("\n".join(shell_scripts) + "\n")
            else:
                f.write(shell_scripts + "\n")
            
            f.write("\n--- Broken Symbolic Links ---\n")
            broken_symlinks = data.get("broken_symlinks", [])
            if isinstance(broken_symlinks, list):
                f.write("\n".join(broken_symlinks) + "\n")
            else:
                f.write(broken_symlinks + "\n")
            
            f.write("\n--- Sensitive PHP Configurations ---\n")
            f.write(data.get("php_configs", "No sensitive configurations found in PHP files.\n"))
            
            f.write("\n--- Backups ---\n")
            backups = data.get("backups", {})
            for key, value in backups.items():
                f.write(f"{key}:\n{value}\n")
        
        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)

