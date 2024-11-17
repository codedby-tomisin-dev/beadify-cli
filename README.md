# Beadify CLI

[![PyPI version](https://img.shields.io/pypi/v/beadify.svg)](https://pypi.org/project/beadify/)
![Python Versions](https://img.shields.io/pypi/pyversions/beadify.svg)
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/beadify) -->
![License](https://img.shields.io/pypi/l/beadify)

Beadify CLI is a lightweight, efficient tool tailored for hobbyists looking to deploy multiple applications on a single Ubuntu-based VPS (Virtual Private Server). This documentation guides you through deploying and managing multiple apps on a single VPS using Beadify CLI.


---
## Table of Contents
1. [Pre-requisites](#pre-requisites)
   - [VPS](#vps)
   - [Local Machine](#local-machine)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Commands Overview](#commands-overview)
   - [Workflow](#workflow)
     - [Initialize a Project](#initialize-a-project)
     - [Specify the Target Machine](#specify-the-target-machine)
     - [Deploy a Bead](#deploy-a-bead)
     - [Run a Bead](#run-a-bead)
     - [Apply SSL](#apply-ssl)
4. [Examples](#examples)
   - [Initializing a Project](#1-initializing-a-project)
   - [Setting Up the Target Host](#2-setting-up-the-target-host)
   - [Deploying an Application](#3-deploying-an-application)
   - [Running the Application](#4-running-the-application)
   - [Setting Up HTTPS](#5-setting-up-https)
5. [Setup](#setup)
6. [Build](#build)
7. [Run](#run)
   - [Source Mode](#source-mode)
   - [Packaged Mode](#packaged-mode)
8. [Troubleshooting](#troubleshooting)
---


## Pre-requisites
### VPS
Currently, the following packages need to be pre-installed on the VPS:
1. Docker
2. Docker Compose
3. Nginx

> Support for automatically installing the required packages will be provided in the coming months.

### Local Machine
1. Python >= 3.9

## Installation
```bash
pip install beadify
```


## Usage

### Commands Overview

The Beadify CLI provides the following commands:

| Command     | Description                                           |
|-------------|-------------------------------------------------------|
| `init`        | Initialize a project for deployment setup             |
| `set-host`    | Specify the target VPS for deploying the project      |
| `provision`   | Deploy a bead (application) to the VPS                |
| `run`         | Run a deployed bead                                   |
| `apply-ssl`   | Apply SSL to the deployed application                 |

### Workflow
#### Initialize a Project
This command creates a manifest file in your project's directory, and sets up a new project for deployment.

```
beadify init --name <service_name>
```

- `--name`: (Required) The name of the service you are deploying.

#### Specify the Target Machine
Configures the target VPS for deployment.

```
beadify set-host --ip <ip_address> --ssh-key-file <path_to_ssh_key> --username <username>
```

- `--ip`: (Required) IP address of the target VPS.  
- `--ssh-key-file`: (Required) Path to your SSH key file.  
- `--username`: (Required) Username for SSH access.

#### Deploy a Bead
Deploys the specified bead (application) to the configured VPS.

```
beadify provision [--domain-name <domain_name>] [--env-file <path_to_env_file>] [--image <docker_image>]
```

- `--domain-name`: (Optional) Domain name for the deployment. Required only once per project.
- `--env-file`: (Optional) Path to the environment variables file. Required only once per project.
- `--image`: (Optional) Docker image to deploy. Only required the first time. Required only once per project.

> You would need a domain name and a Docker image to provision a bead

#### Run a Bead
Runs the deployed bead on the target VPS.

```
beadify run
```

- Starts the service on the configured VPS.

#### Apply SSL
Automatically applies an SSL certificate to your deployed application.

```
beadify apply-ssl
```

- This command uses Let's Encrypt to secure your application with HTTPS.


### Examples

#### 1. Initializing a Project
```
beadify init --service-name my_app
```

#### 2. Setting Up the Target Host
```
beadify set-host --ip 203.0.113.10 --ssh-key-file ~/.ssh/my-vps-ssh-file --username ubuntu
```

#### 3. Deploying an Application
```
beadify provision --domain-name example.com --env-file .env --image my_docker_image
```

#### 4. Running the Application
```
beadify run
```

#### 5. Setting Up HTTPS
```
beadify apply-ssl
```

## Setup
1. Install Python 3.9
2. Clone the repo
3. Navigate to the project's directory and create a virtualenv using: `python -m venv .venv && source .venv/bin/activate`


## Build
To build the Beadify CLI, run the following command in your terminal:
```bash
python setup.py build
```
This will create a bundled version of the CLI tool that can be used as a standalone executable.


## Run
### Source Mode
If you’re developing or testing the CLI, you can run it directly from the source using:
```bash
python -m src.cli {COMMAND} ...
```
This is ideal during development when the CLI is not yet packaged.

### Packaged Mode
Once the CLI is built and bundled, navigate to the directory of a project and:
```bash
/path/to/build/beadify {COMMAND}
```


## Troubleshooting
The Beadify CLI simplifies the process of deploying applications by automating configuration and deployment steps. Make sure to follow the instructions carefully to set up your environment correctly.

Note: Ensure that your VPS and container registry credentials are correctly set up before running the bead deploy command to avoid any authentication issues.
