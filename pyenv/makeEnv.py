# This script sets up and deploys a vurtual environment for python development
# All needed modules will be installed automatically
# The script is cross-platform (Windows/Unix)
# You will enter venv right after executing the script

import os
import sys
import subprocess
import venv
from pathlib import Path

# Define virtual environment directory and list of modules
venv_dir = Path(__file__).parent / "venv"
modules = ["bs4", "requests", "selenium", "webdriver-manager", "psycopg2"]

# Create virtual environment
print(f"Creating virtual environment in ./{venv_dir}")
# print(f"Absolute path: {venv_dir}")
venv.EnvBuilder(with_pip=True).create(venv_dir)

# Define platform-specific paths
if os.name == 'nt':  # For Windows
    pip_path = os.path.join(venv_dir, 'Scripts', 'pip.exe')
    python_path = os.path.join(venv_dir, 'Scripts', 'python.exe')
else:  # For Unix or MacOS
    pip_path = os.path.join(venv_dir, 'bin', 'pip')
    python_path = os.path.join(venv_dir, 'bin', 'python')

# Install modules
print(f"Installing modules: {modules}...")
subprocess.check_call([pip_path, 'install'] + modules)

# # Feedback
# print("Virtual environment setup complete!")
# print(f"To activate it, run:\n\n  source {venv_dir}\\bin\\activate  \t# Unix/macOS")
# print(f"  .\\{venv_dir}\\Scripts\\activate.bat  \t# Windows\n")

# Deploy venv
print("\nVirtual environment setup complete. Launching shell...\n")
if sys.platform == "win32":
    # Launch cmd with activated venv
    activate_script = venv_dir / "Scripts" / "activate.bat"
    subprocess.run(["cmd.exe", "/k", str(activate_script)])
else:
    # Launch bash shell with virtualenv activated
    activate_script = venv_dir / "bin" / "activate"
    bash_command = f"source {activate_script} && exec $SHELL"
    subprocess.run(["bash", "-c", bash_command])