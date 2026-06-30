# macroos
# 🛠️ Macro-OS CLI

**Macro-OS** is a lightweight and extensible multi-tool with a Command Line Interface (CLI) written in Python. The project is designed for quick access to system functions (e.g., Wi-Fi scanning), note management, and environment customization right from the terminal.

## 🚀 Features

The project is designed to be highly flexible. The current core functionality includes:
* **Cross-platform compatibility:** Works seamlessly on Windows, Linux, and macOS (e.g., adaptive network scanning).
* **Note Manager:** A built-in system for quickly saving and reading text data without leaving the terminal.
* **Dynamic settings:** Change your username and interface prompt on the fly, with auto-saving to a configuration file (`config.json`).
* **Modular architecture:** Command routing is built using dictionaries, allowing you to add a new function to the system in literally two lines of code.

## ⚙️ Installation and Setup

No third-party libraries are required to run the program, only standard Python tools.

1. Ensure you have **Python 3.x** installed.
2. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/macro-os.git](https://github.com/YOUR_USERNAME/macro-os.git)
   cd macro-os

   Run the script:

Bash
python macro_os.py
(On some Linux/macOS systems, you may need to use python3 instead of python)

📖 How to Use
To avoid duplicating documentation, the program is self-documenting. After launching, simply type:

Bash
help
This command will display an up-to-date list of all available utilities and their usage syntax.

👨‍💻 For Developers (Adding a custom command)
Adding new features is extremely straightforward. If you want to add your own utility:

Write a function that takes arguments (e.g., def my_tool(args: str) -> str:).

Register it in the commands dictionary inside the handle_command function.

Done! The parser will automatically start handling it.

Created by programmerpythona.
