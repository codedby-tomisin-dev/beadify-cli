import json
import os
import random

import paramiko

from ..core.constants import MANIFEST_FILE_NAME
from ..core.models import Manifest
from .log_message import log_message


def establish_ssh_connection(host_ip: str, username: str, ssh_key_file: str):
    """Establish an SSH connection and return the client."""
    log_message('INFO', f"*** Establishing SSH connection to {host_ip} ***")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(ssh_key_file)

    ssh_client.connect(
        hostname=host_ip,
        username=username,
        pkey=private_key
    )

    log_message('SUCCESS', "SSH connection established")

    return ssh_client


def execute_remote_command(ssh_client, command: str):
    """Execute a command on the remote server via SSH."""
    """Execute a command on the remote server and stream the output in real-time."""
    log_message('INITIATE', f"Executing command on the server: `{command}`")
    
    # Execute the command
    stdin, stdout, stderr = ssh_client.exec_command(command)
    
    # Get the channel from the stdout
    channel = stdout.channel

    # Continuously read from stdout and stderr while the command is running
    while not channel.exit_status_ready():
        # Stream stdout in real-time
        while channel.recv_ready():
            output = stdout.readline()
            if output:
                log_message('INFO', output.strip())

        # Stream stderr in real-time
        while channel.recv_stderr_ready():
            error = stderr.readline()
            if error:
                log_message('INFO', f"Error: {error.strip()}")

    # Ensure any remaining output is printed after the command completes
    stdout_lines = stdout.readlines()
    stderr_lines = stderr.readlines()
    if stdout_lines:
        log_message('INFO', "".join(stdout_lines).strip())
    if stderr_lines:
        log_message('INFO', "".join(stderr_lines).strip())


def get_path_to_script(script_name: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, f'../scripts/{script_name}')


def read_env_file(env_file: str) -> str:
    """Read the contents of the environment file."""
    if env_file and os.path.isfile(env_file):
        with open(env_file, 'r') as file:
            return file.read()
    return ''


def requires_manifest_file(func):
    def decorated_function(*args, **kwargs):
        if not os.path.exists(MANIFEST_FILE_NAME):
            log_message('ERROR', "Bead manifest file is not present in this directory. Did you mean to run 'init' first?")
            return

        with open(MANIFEST_FILE_NAME, 'r') as file:
            data = json.loads(file.read())
            manifest = Manifest(**data)
            func(manifest, *args, **kwargs)

    return decorated_function


def uses_ssh_connection(func):
    def decorated_function(manifest: Manifest, *args, **kwargs):
        ssh_client = establish_ssh_connection(manifest.host.ip, manifest.host.username, manifest.host.ssh_key_file)
        func(manifest, ssh_client, *args, **kwargs)

    return decorated_function


def select_container_port():
    return random.randrange(1024, 49151)


def transfer_file(sftp, local_path: str, remote_path: str):
    """Transfer a file to the remote server using SFTP."""
    try:
        log_message('INFO', f"Transferring '{local_path}' to '{remote_path}' on the server...")
        sftp.put(local_path, remote_path)
        log_message('COMPLETE', "File transferred successfully")
    except FileNotFoundError:
        raise FileNotFoundError(f"Local file '{local_path}' not found.")
    except Exception as e:
        raise IOError(f"Failed to transfer file: {e}")
