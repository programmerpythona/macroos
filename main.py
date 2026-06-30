# ---macro-os---
# for GitHub
#
# from programmerpythona
#
# version 0.2
#

import os
import platform
import subprocess
import json

# Configuration constants
CONFIG_FILE = "config.json"
NOTES_FILE = "notes.txt"

def load_settings() -> dict:
    """Loads settings from a JSON file or returns default ones."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"username": "User", "prompt": "->"}

def save_settings(settings: dict):
    """Saves current settings to a JSON file."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def show_help(*args) -> str:
    """Displays the help menu."""
    return (
        "\n=== AVAILABLE COMMANDS ===\n"
        "start          - Initialize the program\n"
        "scan           - Scan and list available Wi-Fi networks\n"
        "note list      - Show all saved notes\n"
        "note add <txt> - Add a new note\n"
        "note clear     - Delete all notes\n"
        "settings       - View current settings\n"
        "set <key> <val>- Change a setting (e.g., set username Admin)\n"
        "help           - Show this help menu\n"
        "exit           - Close the application\n"
    )

def start_program(*args) -> str:
    """Mock initialization command."""
    return "System initialized. Ready for commands. Type 'help' for options."

def scan_wifi(*args) -> str:
    """Scans for available Wi-Fi networks depending on the OS."""
    current_os = platform.system()

    if current_os == "Windows":
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks"], 
                capture_output=True, 
                text=True, 
                encoding="cp866",
                errors="ignore"
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

def manage_notes(args: str) -> str:
    """Handles creating, listing, and clearing notes."""
    if not args:
        return "Usage: note add <text> | note list | note clear"
    
    parts = args.split(maxsplit=1)
    action = parts[0].lower()
    content = parts[1] if len(parts) > 1 else ""

    if action == "add":
        if not content:
            return "Error: Note text cannot be empty."
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return "Note saved successfully."
        
    elif action == "list":
        if not os.path.exists(NOTES_FILE):
            return "No notes found."
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = f.readlines()
        if not notes:
            return "No notes found."
        
        output = "\n=== YOUR NOTES ===\n"
        for i, note in enumerate(notes, 1):
            output += f"{i}. {note.strip()}\n"
        return output
        
    elif action == "clear":
        if os.path.exists(NOTES_FILE):
            os.remove(NOTES_FILE)
        return "All notes cleared."
        
    return "Unknown note command. Use 'note add <text>', 'note list', or 'note clear'."

def show_settings(*args) -> str:
    """Displays current OS settings."""
    settings = load_settings()
    return (
        "\n=== SYSTEM SETTINGS ===\n"
        f"username : {settings.get('username')}\n"
        f"prompt   : {settings.get('prompt')}\n"
        "-----------------------\n"
        "To change: set <key> <value>"
    )

def change_setting(args: str) -> str:
    """Changes a configuration setting."""
    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        return "Usage: set <key> <value> (e.g., set username Admin)"
    
    key = parts[0].lower()
    value = parts[1]
    
    settings = load_settings()
    if key in settings:
        settings[key] = value
        save_settings(settings)
        return f"Setting '{key}' successfully updated to '{value}'."
    else:
        return f"Error: Unknown setting '{key}'. Available keys: {', '.join(settings.keys())}"


def handle_command(user_input: str) -> str:
    """Parses user input and routes it to the appropriate function."""
    parts = user_input.strip().split(maxsplit=1)
    if not parts:
        return ""
        
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # Command Router
    commands = {
        "help": show_help,
        "start": start_program,
        "scan": scan_wifi,
        "note": manage_notes,
        "settings": show_settings,
        "set": change_setting
    }
    
    if cmd in commands:
        # Pass arguments to the function (functions use *args if they don't need them)
        return commands[cmd](args)
    else:
        return f"Error: Command '{cmd}' does not exist. Type 'help' for options."

if __name__ == "__main__":
    # Clear terminal screen based on OS
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    print("=== MULTI-TOOL CLI INTERFACE READY ===")
    print("Type 'start', 'help', 'scan', or 'exit' to quit.\n")
    
    while True:
        # Reload settings dynamically so prompt changes apply immediately
        current_settings = load_settings()
        user_prompt = f"{current_settings.get('username')} {current_settings.get('prompt')} "
        
        user_text = input(user_prompt)

        if user_text.strip().lower() == "exit":
            print("Shutting down. Goodbye!")
            break
            
        if not user_text.strip():
            continue
            
        result = handle_command(user_text)
        print(result)
