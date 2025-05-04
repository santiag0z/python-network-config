# python-network-config

This Python script enables automated configuration across multiple network switches by reading device information from a `hosts` file, commands from a `commands` file, and login details and device type from a `.env` file. It also generates log files to track execution and errors.

**Credits:** This script was developed with the help of AI collaborator [Gemini](https://gemini.google.com/).

## Prerequisites

* **Python 3.x** installed on your system.
* **Python Libraries:**
    * `netmiko`: For establishing SSH connections with network devices.
    * `python-dotenv`: For loading environment variables from the `.env` file.

    You can install these libraries using pip:
    ```bash
    pip install netmiko python-dotenv
    ```

## Configuration

Before running the script, you need to create and configure the following files in the same directory as the `configure.py` script:

1.  **`.env`:** This file contains SSH login information and the device type. Create a file named `.env` and add your credentials and the device type (e.g., `huawei`):

    ```
    SSH_USERNAME=your_username
    SSH_PASSWORD=your_password
    SSH_PORT=22
    DEVICE_TYPE=huawei
    ```

    **Important:** Keep this file secure and avoid sharing it in public repositories.

2.  **`hosts`:** This file contains the list of IP addresses or hostnames of the switches you want to configure. Each address should be on a separate line:

    ```
    192.168.1.10
    192.168.1.11
    switch-lab-01.example.com
    ```

3.  **`commands`:** This file contains the list of commands you want to execute on each switch. Each command should be on a separate line:

    ```
    show version
    show running-config
    configure terminal
    hostname new-switch-name
    exit
    ```

## Execution

1.  Navigate to the directory where you saved the script files in your terminal.
2.  Run the Python script with the following command:

    ```bash
    python configure.py
    ```

3.  The script will attempt to connect to each switch listed in the `hosts` file and execute the commands defined in the `commands` file.
4.  Execution logs will be saved in files within the `log` folder, including a full log and a log containing only errors. Log files will be named with the prefix `log_` and `log_errors_` followed by the execution date and time.
5.  If the `hosts`, `commands`, or `.env` files do not exist, the script will display a warning and create empty files or files with example information.

## Observations

* Ensure that the SSH credentials in the `.env` file have the necessary permissions to execute the desired commands on the switches.
* The script attempts to automatically detect the device type, but you can explicitly specify the `DEVICE_TYPE` in the `.env` file for better compatibility.
* The `expect_string` parameter in the `execute_commands_on_switch` function is set to try common prompts for Huawei switches (`<|>|]`). If you are using other device types and encounter issues, you might need to adjust this parameter in the script.
* The script includes basic error handling for connection and file reading issues. Check the log files for details on any errors that occur.

## Next Steps and Improvements

* Implement reading specific configurations per switch.
* Add verification functionalities after applying commands.
* Implement a rollback system in case of configuration failure.
* Create a more detailed execution report.

Feel free to contribute and improve this script!