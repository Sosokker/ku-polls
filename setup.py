import os
import subprocess
import sys
import argparse


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

def install_virtualenv(python_commands):
    # Set check=True to throw an error if the return code is non-zero (which is an indication of some error happening).
    try:
        subprocess.run([python_commands, "-m", "pip", "install", "--user", "virtualenv"], check=True)
    except:
        print("+++Error Occur when try to install Virtualenv+++")

def create_virtual_environment(env_name, python_command):
    subprocess.run([python_command, "-m", "virtualenv", env_name], check=True)

def customize_virtual_environment():
    env_name = input("Enter a custom virtual environment name (or press Enter for the default): ").strip()
    if not env_name:
        env_name = "venv"
    return env_name

def setup_environment_variables(python_command_in_venv):
    print("Setting up Django environment variables:")

    # SECRET KEY
    generate_secret_key = input("Generate a Django SECRET_KEY? (yes/no): ").strip().lower()
    if generate_secret_key == "yes":
        secret_key = subprocess.check_output([python_command_in_venv, "manage.py", "shell", "-c",
                                             'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())']).decode().strip()
    else:
        secret_key = input("Enter Django SECRET_KEY: ").strip()

    # DEBUG MODE
    while True:
        debug_mode = input("Enable DEBUG mode? (True/False): ").strip()
        if debug_mode in ["True", "False"]:
            break
        else:
            print("Please enter 'True' or 'False' for DEBUG mode. (Case Sensitive)")

    # ALLOWED_HOSTS
    allowed_hosts = input("Enter ALLOWED_HOSTS (comma-separated, or press Enter for default): ").strip()
    if not allowed_hosts:
        allowed_hosts = "*.ku.th,localhost,127.0.0.1,::1"

    # TZ
    available_time_zones = ["Asia/Bangkok", "Japan", "UCT", "CST6CDT", "Custom"]
    
    print("Available time zone options:")
    for idx, tz in enumerate(available_time_zones, start=1):
        print(f"{idx}. {tz}")

    while True:
        try:
            selected_tz_index = int(input("Enter the number for TIME_ZONE: ")) - 1
            if 0 <= selected_tz_index < len(available_time_zones):
                time_zone = available_time_zones[selected_tz_index]
                break
            elif (selected_tz_index == len(available_time_zones)):
                time_zone = input("Please enter you timezone: ")
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    email_host_password = input("Enter EMAIL_HOST_PASSWORD: ").strip()

    # SET
    with open(".env", "w") as env_file:
        env_file.write(f"""SECRET_KEY={secret_key}
        DEBUG={debug_mode}
        ALLOWED_HOSTS={allowed_hosts}
        TIME_ZONE={time_zone}
        EMAIL_HOST_PASSWORD={email_host_password}
        """)

def main():
    parser = argparse.ArgumentParser(description="Django Setup Script")
    parser.add_argument("-custom", action="store_true", help="Enter custom mode")
    args = parser.parse_args()

    python_command = check_python_command()

    if python_command is None:
        print("Error: Python interpreter not found. Please specify the Python command (e.g., python, py, python3).")
        sys.exit(1)

    if not args.custom:
        if python_command is None:
            print("Error: Python interpreter not found. Please specify the Python command (e.g., python, py, python3).")
            sys.exit(1)


        setup_venv = input("Do you want to set up a virtual environment? (yes/no): ").lower()
        if setup_venv == "yes":
            print("==========================Default Mode==========================")
            print("==========================Install Virtualenv==========================")
            install_virtualenv(python_command)
            if not os.path.exists("venv"):
                print("==========================Creating a new virtual environment...==========================")
                subprocess.run([python_command, "-m", "virtualenv", "venv"])
            else:
                print("==========================Using an existing virtual environment.==========================")

            if is_posix:
                activate_command = os.path.join("venv", "bin", "activate")
            elif is_windows:
                activate_command = os.path.join("venv", "Scripts", "activate")
            subprocess.run([activate_command], shell=True)

            python_command = os.path.join("venv", "bin", "python") if is_posix else os.path.join("venv", "Scripts", "python")
        else:
            print("Not setting up a virtual environment. Using the global Python interpreter.")

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
        subprocess.run([python_command, "manage.py", "loaddata", "data/vote.json"])

        start_server = input("Do you want to start the Django server? (yes/no): ").lower()
        if start_server == "yes":
            print("=================================================")
            print("Django run in --insecure mode to load Static File")
            print("==================================================")
            subprocess.run([python_command, "manage.py", "runserver", "--insecure"])
    else:
        try:
            print("==========================Custom Mode==========================")
            python_commands = check_python_command()
            env_name = customize_virtual_environment()
            print("==========================Install Virtualenv==========================")
            install_virtualenv(python_commands)
            create_virtual_environment(env_name, python_commands)
            print(f"Finishing Create Virtual environment {env_name}")
            python_command_in_venv = os.path.join(env_name, "bin", "python") if is_posix else os.path.join(env_name, "Scripts", "python")
            print(f"==========================Install Requirement==========================")
            subprocess.run([python_command_in_venv, "-m", "pip", "install", "-r", "requirements.txt"])
            setup_environment_variables(python_command_in_venv)

            subprocess.run([python_command_in_venv, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            subprocess.run([python_command_in_venv, "manage.py", "migrate"], check=True)
            subprocess.run([python_command_in_venv, "manage.py", "loaddata", "data/users.json"], check=True)
            subprocess.run([python_command_in_venv, "manage.py", "loaddata", "data/polls.json"], check=True)
            subprocess.run([python_command_in_venv, "manage.py", "loaddata", "data/vote.json"], check=True)

            start_server = input("Do you want to start the Django server? (yes/no): ").strip().lower()
            if start_server == "yes":
                print("=================================================")
                print("Django run in --insecure mode to load Static File")
                print("==================================================")
                subprocess.run([python_command_in_venv, "manage.py", "runserver", "--insecure"], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nSetup process aborted.")
            sys.exit(1)


if __name__ == "__main__":
    main()
