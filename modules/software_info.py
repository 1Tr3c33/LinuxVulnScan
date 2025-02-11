import subprocess
import os

def find_useful_software():
    """Searches for useful installed software that can be executed from the terminal."""
    try:
        software = subprocess.getoutput("compgen -c | sort | uniq")
        return software.splitlines() if software else "No available programs found in the terminal."
    except Exception as e:
        return f"Error searching for useful software: {str(e)}"

def find_compilers_and_packages():
    """Searches for installed compilers and vulnerable packages."""
    try:
        # Compilers
        compilers = subprocess.getoutput("which gcc g++ clang make cmake 2>/dev/null")
        # Packages installed via pkg or brew
        pkg_packages = subprocess.getoutput("pkg info 2>/dev/null || echo 'pkg not available'")
        brew_packages = subprocess.getoutput("brew list 2>/dev/null || echo 'brew not available'")
        # Vulnerable packages
        vulnerable_packages = subprocess.getoutput("dpkg -l | grep -i 'vulnerable' 2>/dev/null || echo 'No vulnerable packages found.'")
        
        return {
            "Compilers": compilers if compilers else "No installed compilers found.",
            "Packages via pkg": pkg_packages,
            "Packages via brew": brew_packages,
            "Vulnerable Packages": vulnerable_packages,
        }
    except Exception as e:
        return f"Error searching for compilers and packages: {str(e)}"

def check_ctr_tool():
    """Checks if the ctr tool from containerd is available."""
    try:
        result = subprocess.run(["ctr", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip() if result.returncode == 0 else "ctr is not available."
    except FileNotFoundError:
        return "ctr is not installed on this system."
    except Exception as e:
        return f"Error verifying ctr: {str(e)}"

def find_specific_programs():
    """Searches for specific and useful programs installed on the system."""
    programs = [
        "docker", "kcpassword", "phpsession", "apache2", "kerberos", "pam", "aws", "vault",
        "leak", "git", "postgresql", "dovecot", "log4shell", "rune", "freelpa", "mysql", "skey",
        "gitlab", "pgp", "screen", "splunk", "ssh", "tmux", "vault", "yubikey"
    ]
    found_programs = {}
    for program in programs:
        try:
            result = subprocess.run(["which", program], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            found_programs[program] = "Found" if result.returncode == 0 else "Not found"
        except Exception as e:
            found_programs[program] = f"Error: {str(e)}"
    return found_programs

def create_report_directory():
    """Creates the 'report' folder if it does not exist."""
    report_dir = os.path.join(os.getcwd(), "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def gather_data():
    """Collects all module information and returns it as a dictionary."""
    return {
        "useful_software": find_useful_software(),
        "compilers_and_packages": find_compilers_and_packages(),
        "ctr_tool": check_ctr_tool(),
        "specific_programs": find_specific_programs(),
    }

def generate_report(data, output_file="software_info_report.txt"):
    """Generates a plain text report with the obtained results."""
    try:
        # Create the report directory
        report_dir = create_report_directory()
        report_path = os.path.join(report_dir, output_file)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Software Information Report ===\n")
            
            f.write("\n--- Useful Installed Software ---\n")
            useful_software = data.get("useful_software", [])
            if isinstance(useful_software, list):
                f.write("\n".join(useful_software) + "\n")
            else:
                f.write(useful_software + "\n")
            
            f.write("\n--- Compilers and Packages ---\n")
            compilers_packages = data.get("compilers_and_packages", {})
            for key, value in compilers_packages.items():
                f.write(f"{key}:\n{value}\n")
            
            f.write("\n--- Verification of ctr Tool ---\n")
            f.write(data.get("ctr_tool", "Could not verify the ctr tool.\n"))
            
            f.write("\n--- Specific Programs ---\n")
            specific_programs = data.get("specific_programs", {})
            for program, status in specific_programs.items():
                f.write(f"{program}: {status}\n")
        
        print(f"[+] Report generated: {report_path}")
    except Exception as e:
        print(f"[-] Error generating the report: {str(e)}")

if __name__ == "__main__":
    data = gather_data()
    generate_report(data)

