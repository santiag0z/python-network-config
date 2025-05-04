import netmiko
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
USERNAME = os.getenv("SSH_USERNAME")
PASSWORD = os.getenv("SSH_PASSWORD")
SSH_PORT = os.getenv("SSH_PORT")
DEVICE_TYPE = os.getenv("DEVICE_TYPE")

# Define the log folder name
LOG_FOLDER = "log"

# Create the log folder if it doesn't exist
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# Get the date and time for the log file name
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Base name for the log files
log_base_name = os.path.join(LOG_FOLDER, f"{timestamp}")
error_log_base_name = os.path.join(LOG_FOLDER, f"{timestamp}_errors")

# Configure the main logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler for the full log
full_log_file = f"{log_base_name}.log"
file_handler_all = logging.FileHandler(full_log_file)
file_handler_all.setFormatter(formatter)
logger.addHandler(file_handler_all)

# Handler for the error log
error_log_file = f"{error_log_base_name}.log"
file_handler_error = logging.FileHandler(error_log_file)
file_handler_error.setFormatter(formatter)
file_handler_error.setLevel(logging.ERROR)  # Set level to ERROR
logger.addHandler(file_handler_error)

def read_hosts(filename="hosts"):
    """Reads the list of hosts from the file. Creates an empty one if not found."""
    try:
        with open(filename, "r") as f:
            hosts = [line.strip() for line in f if line.strip()]
        return hosts
    except FileNotFoundError:
        logger.warning(f"File '{filename}' not found. Creating an empty '{filename}' file.")
        with open(filename, "w") as f:
            pass
        return []

def read_commands(filename="commands"):
    """Reads the list of commands from the file. Creates an empty one if not found."""
    try:
        with open(filename, "r") as f:
            commands = [line.strip() for line in f if line.strip()]
        return commands
    except FileNotFoundError:
        logger.warning(f"File '{filename}' not found. Creating an empty '{filename}' file.")
        with open(filename, "w") as f:
            pass
        return []

# Check and create the .env file if it doesn't exist
if not os.path.exists(".env"):
    logger.warning("File '.env' not found. Creating a '.env' file with example information. Please edit this file with your credentials.")
    with open(".env", "w") as f:
        f.write("SSH_USERNAME=your_username\n")
        f.write("SSH_PASSWORD=your_password\n")
        f.write("SSH_PORT=22\n")
        f.write("DEVICE_TYPE=huawei\n")

def execute_commands_on_device(host, commands, expect_string="<|>|]"):
    """Executes the list of commands on a specific device."""
    ssh_config = {
        "device_type": DEVICE_TYPE,
        "host": host,
        "username": USERNAME,
        "password": PASSWORD,
        "port": SSH_PORT,
        "timeout": 10,
        "conn_timeout": 5,
    }
    try:
        logger.info(f"Connecting to device: {host}")
        with netmiko.ConnectHandler(**ssh_config) as net_connect:
            logger.info(f"Connection established with: {host}")
            for command in commands:
                logger.info(f"Sending command '{command}' to {host}")
                output = net_connect.send_command(command, expect_string=expect_string, read_timeout=30)
                logger.info(f"Response from {host} for '{command}':\n{output.strip()}")
        logger.info(f"Commands executed successfully on: {host}")
        return True
    except netmiko.NetmikoTimeoutException:
        logger.error(f"Timeout while connecting to: {host}")
        return False
    except netmiko.NetmikoAuthenticationException:
        logger.error(f"Authentication error while connecting to: {host}")
        return False
    except Exception as e:
        logger.error(f"An error occurred while connecting or executing commands on {host}: {e}")
        return False

if __name__ == "__main__":
    hosts = read_hosts()
    commands = read_commands()
    load_dotenv()  # Ensure .env is loaded again after potential creation

    USERNAME = os.getenv("SSH_USERNAME")
    PASSWORD = os.getenv("SSH_PASSWORD")
    SSH_PORT = os.getenv("SSH_PORT")
    DEVICE_TYPE = os.getenv("DEVICE_TYPE")

    if not hosts:
        print("No hosts found in the 'hosts' file.")
    elif not commands:
        print("No commands found in the 'commands' file.")
    elif not DEVICE_TYPE:
        print("The DEVICE_TYPE variable is not defined in the .env file. Please add DEVICE_TYPE=your_device_type to the '.env' file.")
    else:
        print(f"Starting configuration for devices of type: {DEVICE_TYPE}")
        prompt_expected = "<|>|]"
        for host in hosts:
            print(f"\nConfiguring device: {host}")
            execute_commands_on_device(host, commands, expect_string=prompt_expected)
        print(f"\nConfiguration process completed. Logs have been saved in the '{LOG_FOLDER}' folder.")