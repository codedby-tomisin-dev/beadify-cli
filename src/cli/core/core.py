from paramiko import SSHClient

from .helpers import (
    execute_remote_command,
    get_path_to_script,
    read_env_file,
    requires_manifest_file,
    select_container_port,
    transfer_file,
    uses_ssh_connection
)
from .log_message import log_message
from .models import Manifest


def initialise_project(name: str):
    manifest = Manifest(name=name)
    manifest.save()

    log_message('SUCCESS', 'Bead initiated successfully!')


@requires_manifest_file
def set_host(manifest: Manifest, username: str, ip: str, ssh_key_file: str, domain_name: str):
    manifest.host = Manifest.Host(**{
        'username': username,
        'ip': ip,
        'ssh_key_file': ssh_key_file,
        'domain_name': domain_name
    })
    manifest.save()

    log_message('SUCCESS', 'Host set successfully!')


@requires_manifest_file
@uses_ssh_connection
def deploy_bead(manifest: Manifest, ssh_client: SSHClient, env_file: str = None, image: str = None):
    container_port = manifest.container_port or select_container_port()
    domain_name = manifest.host.domain_name
    env_file = env_file or manifest.env_file
    image = image or manifest.image

    if not domain_name:
        raise ValueError('A domain name is required')
    if not image:
        raise ValueError('An image is required')

    try:
        with ssh_client.open_sftp() as sftp:
            bead_script_local_path = get_path_to_script('add_bead_to_server.py')
            bead_script_remote_path = '/tmp/add_bead_to_server.py'
            transfer_file(sftp, bead_script_local_path, bead_script_remote_path)

            log_message()

            env_file_content = read_env_file(env_file, encode=True) if env_file else None

            run_deploy_script_cmd = (
                f"sudo python3 {bead_script_remote_path} "
                f"--name {manifest.name} "
                f"--domain-name {domain_name} "
                f"--container-port {container_port} "
                f"--image {image} "
                f"{'--env-file-content ' + env_file_content if env_file_content else ''}"
            )

            execute_remote_command(ssh_client, run_deploy_script_cmd)
    except:
        ssh_client.close()
        return
    finally:
        ssh_client.close()

    log_message()

    manifest.container_port = container_port
    manifest.env_file = env_file
    manifest.host.domain_name = domain_name
    manifest.image = image
    manifest.save()

    log_message('SUCCESS', f"\n✅ Successfully added bead '{manifest.name}'. Run 'beadify run' to launch the service")


@requires_manifest_file
@uses_ssh_connection
def obtain_ssl_certificate(manifest: Manifest, ssh_client):
    log_message('INITIATE', 'Obtaining SSL certificate')

    if not manifest.host.domain_name:
        raise ValueError("`domain_name` not found in manifest. Did you mean to run `provision` first?")

    execute_remote_command(ssh_client, f"sudo certbot --nginx -d {manifest.host.domain_name}")

    log_message('SUCCESS', f'🔐 HTTPS enabled for your service: https://{manifest.host.domain_name}')


@requires_manifest_file
@uses_ssh_connection
def run(manifest: Manifest, ssh_client):
    log_message('INFO', '----------------------------------------------\n')

    execute_remote_command(ssh_client, f"docker-compose -f /beads/{manifest.name}.yml up -d --pull always --force-recreate && sudo systemctl reload nginx")

    log_message('SUCCESS', f'🟢 Bead is now running: http://{manifest.host.domain_name}')


@requires_manifest_file
@uses_ssh_connection
def logs(manifest: Manifest, ssh_client):
    log_message('INITIATE', 'Fetching logs...')

    execute_remote_command(ssh_client, f"docker-compose -f /beads/{manifest.name}.yml logs --tail=100 --follow")


def provision(username: str, ip: str, ssh_key_file: str):
    """
    INSTALLATIONS
    - Install Nginx
    - Install Docker
    - Install Docker Compose
    - Install certbot

    EXECUTIONS
    - Start Nginx
    """

    pass
