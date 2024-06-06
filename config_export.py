import paramiko
import time
import os
from stat import S_ISDIR

# List of IP addresses and their respective root passwords
machines = [
    {"ip": "YOUR_IP", "password": "YOUR_PASSWORD"},
]

# Directory to store the downloaded files (relative to the script's location)
base_download_directory = "keys/mlnl"


# Function to create directories if they don't exist
def create_directory(directory):
    os.makedirs(directory, exist_ok=True)


# Function to recursively download a directory
def download_directory(sftp, remote_dir, local_dir):
    for entry in sftp.listdir_attr(remote_dir):
        remote_entry_path = os.path.join(remote_dir, entry.filename)
        local_entry_path = os.path.join(local_dir, entry.filename)
        if S_ISDIR(entry.st_mode):  # Check if it's a directory
            create_directory(local_entry_path)
            download_directory(sftp, remote_entry_path, local_entry_path)
        else:
            sftp.get(remote_entry_path, local_entry_path)


# Create the base download directory
create_directory(base_download_directory)

# Iterate over each machine
for machine in machines:
    ip = machine["ip"]
    password = machine["password"]

    print(f"\nConnecting to {ip}...")

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the machine
        ssh.connect(ip, username="root", password=password)

        print(f"Connected to {ip}")

        # Create the directory for the current IP
        ip_directory = os.path.join(base_download_directory, ip)
        create_directory(ip_directory)

        # Navigate to the .config directory and download keys.yml and config.yml
        sftp = ssh.open_sftp()
        sftp.chdir("/root/ceremonyclient/node/.config")

        # Download keys.yml
        remote_path = "keys.yml"
        local_path = os.path.join(ip_directory, "keys.yml")
        sftp.get(remote_path, local_path)
        print(f"Downloaded keys.yml from {ip}")

        # Download config.yml
        remote_path = "config.yml"
        local_path = os.path.join(ip_directory, "config.yml")
        sftp.get(remote_path, local_path)
        print(f"Downloaded config.yml from {ip}")

        # Download the entire 'store' directory
        store_remote_path = "/root/ceremonyclient/node/.config/store"
        store_local_path = os.path.join(ip_directory, "store")
        create_directory(store_local_path)  # Ensure local directory exists

        # Call the function to download the 'store' directory
        download_directory(sftp, store_remote_path, store_local_path)
        print(f"Downloaded store directory from {ip}")

        sftp.close()

    except paramiko.AuthenticationException:
        print(f"Authentication failed for {ip}")
    except paramiko.SSHException as e:
        print(f"SSH connection failed for {ip}: {str(e)}")
    finally:
        # Close the SSH connection
        ssh.close()

    # Add a delay between each machine (optional)
    time.sleep(2)

print("\nScript execution completed on all machines.")
