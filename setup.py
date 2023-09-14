import os
import subprocess
import sys

is_windows = os.name == 'nt'
is_posix = os.name == 'posix'

def check_python_command():
    python_commands = ["python", "py", "python3"]
    
    for command in python_commands:
        try:
            subprocess.check_output([command, "--version"])
            return command
        except FileNotFoundError:
            continue
    
    return None

python_command = check_python_command()

if python_command is None:
    print("Error: Python interpreter not found. Please specify the Python command (e.g., python, py, python3).")
    sys.exit(1)

setup_venv = input("Do you want to set up a virtual environment? (yes/no): ").lower()
if setup_venv == "yes":
    if not os.path.exists(".venv"):
        print("Creating a new virtual environment...")
        subprocess.run([python_command, "-m", "venv", ".venv"])
    else:
        print("Using an existing virtual environment.")

    if is_posix:
        activate_command = os.path.join(".venv", "bin", "activate")
    elif is_windows:
        activate_command = os.path.join(".venv", "Scripts", "activate")
    subprocess.run([activate_command], shell=True)

subprocess.run([python_command, "-m", "pip", "install", "-r", "requirements.txt"])

secret_key = subprocess.check_output([python_command, "manage.py", "shell", "-c",
                                     'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())']).decode().strip()

with open(".env", "w") as env_file:
    env_file.write(f"""SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS=*.ku.th,localhost,127.0.0.1,::1
TIME_ZONE=Asia/Bangkok
EMAIL_HOST_PASSWORD=temppassword
""")

subprocess.run([python_command, "manage.py", "migrate"])
subprocess.run([python_command, "manage.py", "loaddata", "data/users.json"])
subprocess.run([python_command, "manage.py", "loaddata", "data/polls.json"])

start_server = input("Do you want to start the Django server? (yes/no): ").lower()
if start_server == "yes":
    print("=================================================")
    print("Django run in --insecure mode to load Static File")
    print("==================================================")
    subprocess.run([python_command, "manage.py", "runserver", "--insecure"])
