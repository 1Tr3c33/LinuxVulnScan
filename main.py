import sys

# Import the created modules
from modules import container_info
from modules import crons_timers
from modules import interesting_files
from modules import network_info
from modules import perm_files
from modules import software_info
from modules import system_info
from modules import users_info


def display_help():
    """Displays the help panel with module information."""
    help_text = """
    ==========================================
                 Linux VulnScan
    ==========================================
    Available options:
    1. Scan containers (container_info).
    2. Scan cron jobs and timers (crons_timers).
    3. Scan for interesting files (interesting_files).
    4. Analyze network information (network_info).
    5. Analyze file permissions (perm_files).
    6. Analyze software information (software_info).
    7. Analyze system information (system_info).
    8. Analyze user information (users_info).
    9. Execute all modules (Full Scan).
    10. Exit.

    All results will be saved in automatically generated plain text reports.
    """
    print(help_text)


def execute_module(module, module_name):
    """Runs a module, collects the data, and generates its report."""
    try:
        print(f"\n[+] Running {module_name}...")
        data = module.gather_data()  # Collect data from the module
        module.generate_report(data)  # Generate a report based on the data
        print(f"[+] Module {module_name} executed successfully.\n")
    except AttributeError as e:
        print(f"[-] Error: The module {module_name} does not have the expected function: {str(e)}")
    except Exception as e:
        print(f"[-] Unexpected error while executing {module_name}: {str(e)}")


def main():
    """Main management of the application."""
    while True:
        display_help()
        try:
            option = int(input("Select an option (1-10): "))
            
            if option == 1:
                execute_module(container_info, "Container Analysis")
            elif option == 2:
                execute_module(crons_timers, "Cron Jobs and Timers")
            elif option == 3:
                execute_module(interesting_files, "Interesting Files")
            elif option == 4:
                execute_module(network_info, "Network Information")
            elif option == 5:
                execute_module(perm_files, "File Permissions")
            elif option == 6:
                execute_module(software_info, "Software Information")
            elif option == 7:
                execute_module(system_info, "System Information")
            elif option == 8:
                execute_module(users_info, "User Information")
            elif option == 9:
                print("\n[+] Running all modules...")
                execute_module(container_info, "Container Analysis")
                execute_module(crons_timers, "Cron Jobs and Timers")
                execute_module(interesting_files, "Interesting Files")
                execute_module(network_info, "Network Information")
                execute_module(perm_files, "File Permissions")
                execute_module(software_info, "Software Information")
                execute_module(system_info, "System Information")
                execute_module(users_info, "User Information")
                print("[+] Full analysis completed.\n")
            elif option == 10:
                print("Exiting the application. Goodbye!")
                sys.exit(0)
            else:
                print("[-] Invalid option. Please select a number between 1 and 10.")
        except ValueError:
            print("[-] Please enter a valid number.")


if __name__ == "__main__":
    main()

