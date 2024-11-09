import argparse
import os
import subprocess
from typing import Literal


DOCKER_COMPOSE_MANIFEST_DIRECTORY = '/beads'


def log_message(type: Literal['SUCCESS', 'INFO', 'INITIATE', 'ERROR', 'COMPLETE'], msg: str):
    style = {
        'COMPLETE': '\033[94m',
        'INITIATE': '\033[96m',
        'ERROR': '\033[91m'
    }.get(type, '')
            
    print(f'{style}{msg}')


def validate_service_name(service_name: str):
    """Validate that the service name contains only alphanumeric characters or underscores."""
    if not all(char.isalnum() or char == '_' for char in service_name):
        raise ValueError("Service name can only contain letters, numbers, and underscores")


def create_directory(dir: str):
    """Create the Docker Compose manifest directory if it does not exist."""
    if not os.path.exists(dir):
        process = subprocess.run(
            ['mkdir', '-p', dir],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        log_message('INFO', process.stdout)


def write_docker_compose_file(service_name: str, container_port: str, image: str):
    """Write the Docker Compose file for the specified service."""
    docker_compose_file_path = f'{DOCKER_COMPOSE_MANIFEST_DIRECTORY}/{service_name}.yml'
    content = f"""services:
  {service_name}:
    container_name: '{service_name}'
    image: {image}
    ports:
      - "{container_port}:80"
    env_file:
      - /etc/{service_name}/.env
    restart: always
"""
    with open(docker_compose_file_path, 'w') as file:
        file.write(content)

    log_message('COMPLETE', f'Written Docker Compose manifest file: {docker_compose_file_path}')


def write_env_file(dir: str, content: str):
    create_directory(dir)

    with open(f'{dir}/.env', 'w') as file:
        file.write(content or '')

    log_message('COMPLETE', 'Written env file')


def write_nginx_config(service_name: str, domain_name: str, container_port: str):
    """Write the Nginx configuration file for the service."""
    nginx_config_file = f'/etc/nginx/sites-available/{service_name}'
    server_config_block = f"""server {{
    server_name {domain_name};

    # Proxy requests to the Docker container running on the specified port
    location / {{
        proxy_pass http://127.0.0.1:{container_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
    with open(nginx_config_file, 'w') as file:
        file.write(server_config_block)
    log_message('COMPLETE', f'Written server configuration to: {nginx_config_file}')

    subprocess.run(['nginx', '-t'], check=True)


def create_nginx_symlink(service_name: str):
    """Create a symbolic link for Nginx to enable the new site, removing any existing symlink."""
    src = f'/etc/nginx/sites-available/{service_name}'
    dest = f'/etc/nginx/sites-enabled/{service_name}'
    
    try:
        # Check if the symlink already exists
        if os.path.islink(dest):
            os.remove(dest)

        # Create a new symlink
        subprocess.run(['ln', '-s', src, dest], check=True)
        log_message('COMPLETE', f'Enabled site {service_name} on Nginx')

    except FileNotFoundError:
        log_message('ERROR', f"Source file {src} does not exist.")
    except subprocess.CalledProcessError as e:
        log_message('ERROR', f"Error creating Nginx symlink: {e}")
    except Exception as e:
        log_message('ERROR', f"Unexpected error: {e}")


def run(service_name: str, domain_name: str, env_file_content: str, container_port: str, image: str):
    """Orchestrate the creation of the Docker and Nginx configurations."""

    validate_service_name(service_name)
    write_env_file(f'/etc/{service_name}', env_file_content)
    create_directory(DOCKER_COMPOSE_MANIFEST_DIRECTORY)
    write_docker_compose_file(service_name, container_port, image)
    write_nginx_config(service_name, domain_name, container_port)
    create_nginx_symlink(service_name)


def main():
    parser = argparse.ArgumentParser(description="A script that handles arguments.")
    parser.add_argument('--service-name', type=str, help="Service name", required=True)
    parser.add_argument('--domain-name', type=str, help="Domain name", required=True)
    parser.add_argument('--env-file-content', type=str, help="Env file content", required=False)
    parser.add_argument('--container-port', type=str, help="Container port", required=True)
    parser.add_argument('--image', type=str, help="Docker image", required=True)
    
    args = parser.parse_args()
    run(args.service_name, args.domain_name, args.env_file_content, args.container_port, args.image)


if __name__ == '__main__':
    main()
