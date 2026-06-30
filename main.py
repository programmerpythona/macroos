#---macro-os---
#for GitHub
#
#from programmerpythona
#
#version 0.1
#

import os
import platform
import subprocess

def show_help():
    return (
        "\n=== AVAILABLE COMMANDS ===\n"
        "start  - Initialize the program\n"
        "help   - Show this help menu\n"
        "scan   - Scan and list available Wi-Fi networks\n"
        "exit   - Close the application\n"
    )

def start_program():
    return "System initialized. Ready for commands. Type 'scan' to analyze Wi-Fi."

def scan_wifi():
    current_os = platform.system()

    if current_os == "Windows":
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks"], 
                capture_output=True, 
                text=True, 
                encoding="cp866"
            )
            return f"\n=== AVAILABLE WI-FI NETWORKS ===\n{result.stdout}"
        except Exception as e:
            return f"Error scanning Wi-Fi on Windows: {e}"
            

    elif current_os == "Linux":
        try:
            result = subprocess.run(["nmcli", "dev", "wifi"], capture_output=True, text=True)
            return f"\n=== AVAILABLE WI-FI NETWORKS ===\n{result.stdout}"
        except FileNotFoundError:
            return "Error: 'nmcli' tool not found. Install network-manager or run as root."
        except Exception as e:
            return f"Error scanning Wi-Fi on Linux: {e}"
            

    elif current_os == "Darwin":
        try:
            airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
            result = subprocess.run([airport_path, "-s"], capture_output=True, text=True)
            return f"\n=== AVAILABLE WI-FI NETWORKS ===\n{result.stdout}"
        except Exception as e:
            return f"Error scanning Wi-Fi on macOS: {e}"
            
    else:
        return f"Unsupported Operating System: {current_os}"



def handle_command(user_input):
    commands = {
        "help": show_help,
        "start": start_program,
        "scan": scan_wifi
    }
    
    cmd = user_input.strip().lower()
    
    if cmd in commands:
        return commands[cmd]()
    else:
        return f"Error: Command '{cmd}' does not exist. Type 'help' for options."


if __name__ == "__main__":

    os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    print("=== MULTI-TOOL CLI INTERFACE READY ===")
    print("Type 'start', 'help', 'scan', or 'exit' to quit.\n")
    
    while True:
        user_text = input("Enter command -> ")

        if user_text.strip().lower() == "exit":
            print("Shutting down. Goodbye!")
            break
            
        if not user_text.strip():
            continue
            
        result = handle_command(user_text)
        print(result)
