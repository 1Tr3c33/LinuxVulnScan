import os
import re
import subprocess

# Definir patrones de regex para detectar archivos sensibles
FILE_PATTERNS = [
    r".*config.*", r".*\.env", r".*\.ini", r".*\.log", r".*\.json",
    r".*\.yml", r".*\.xml", r".*\.bak", r".*\.backup", r".*\.old",
    r".*\.save", r".*\.cred", r".*\.key", r".*\.token", r".*\.secret", r".*\.pass"
]

# Definir patrones de regex para detectar claves API y credenciales
API_KEY_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws_secret_access_key\s*=\s*['\"]?[A-Za-z0-9\/+=]{40}['\"]?",
    "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
    "Google OAuth Token": r"ya29\.[0-9A-Za-z\-_]+",
    "Generic API Key": r"(?i)(api_key|apikey|secret|token)\s*=\s*['\"]?[A-Za-z0-9-_.]{10,100}['\"]?",
    "GitHub Token": r"ghp_[0-9A-Za-z]{36}",
    "Slack Token": r"xox[baprs]-[0-9A-Za-z]{10,48}",
    "Stripe API Key": r"(?i)(sk_live|pk_live)_[0-9a-zA-Z]{24}",
    "Azure Access Token": r"eyJ[A-Za-z0-9]{30,1000}\.[A-Za-z0-9]{10,1000}\.[A-Za-z0-9_-]{10,1000}",
}

# Directorios a escanear
SCAN_DIRECTORIES = ["/home", "/etc", "/var/www", "/root", "/opt"]

def find_interesting_files():
    """Search for files matching sensitive patterns using regex."""
    found_files = []
    
    for directory in SCAN_DIRECTORIES:
        if os.path.exists(directory):
            try:
                grep_pattern = "|".join(FILE_PATTERNS)
                search_result = subprocess.getoutput(f"find {directory} -type f | grep -Ei '{grep_pattern}' 2>/dev/null")
                if search_result:
                    found_files.extend(search_result.split("\n"))
            except Exception as e:
                found_files.append(f"Error searching in {directory}: {str(e)}")

    return found_files if found_files else "No sensitive files found."

def search_api_keys(files):
    """Search for API keys and credentials inside the found files."""
    results = {}

    for file in files:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for key_type, pattern in API_KEY_PATTERNS.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        if file not in results:
                            results[file] = []
                        results[file].extend([f"{key_type}: {match}" for match in matches])
        except Exception:
            pass  # Evitar errores de archivos protegidos

    return results if results else "No API keys or credentials found."

def find_broken_symlinks():
    """Identifies broken symbolic links in the system."""
    try:
        broken_symlinks = subprocess.getoutput("find / -xtype l 2>/dev/null")
        return broken_symlinks if broken_symlinks else "No broken symbolic links found."
    except Exception as e:
        return f"Error searching for broken symbolic links: {str(e)}"

def list_temp_files():
    """Lists files in temporary directories that might contain sensitive information."""
    try:
        temp_files = subprocess.getoutput("ls -lah /tmp/ /var/tmp/ 2>/dev/null")
        return temp_files if temp_files else "No temporary files found."
    except Exception as e:
        return f"Error listing temporary files: {str(e)}"

def create_report_directory():
    """Creates the 'report' directory if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    print("[+] Searching for interesting files...")
    interesting_files = find_interesting_files()

    print("[+] Searching for API keys inside found files...")
    api_key_results = search_api_keys(interesting_files if isinstance(interesting_files, list) else [])

    print("[+] Searching for broken symbolic links...")
    broken_symlinks = find_broken_symlinks()

    print("[+] Listing temporary files...")
    temp_files = list_temp_files()

    return {
        "Interesting Files": interesting_files,
        "API Keys & Credentials": api_key_results,
        "Broken Symbolic Links": broken_symlinks,
        "Temporary Files": temp_files,
    }

def generate_report(data, output_file="interesting_files_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Improved Interesting Files Report ===\n")

            f.write("\n--- Interesting Files ---\n")
            if isinstance(data["Interesting Files"], list):
                f.write("\n".join(data["Interesting Files"]) + "\n")
            else:
                f.write(data["Interesting Files"] + "\n")

            f.write("\n--- API Keys & Credentials Found ---\n")
            if isinstance(data["API Keys & Credentials"], dict):
                for file, keys in data["API Keys & Credentials"].items():
                    f.write(f"{file}:\n" + "\n".join(keys) + "\n")
            else:
                f.write(data["API Keys & Credentials"] + "\n")

            f.write("\n--- Broken Symbolic Links ---\n")
            f.write(data["Broken Symbolic Links"] + "\n")

            f.write("\n--- Temporary Files ---\n")
            f.write(data["Temporary Files"] + "\n")

        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)


