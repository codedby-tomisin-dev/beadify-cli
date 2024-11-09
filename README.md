# Beads CLI
Beads CLI is a fast and efficient tool designed for deploying lightweight applications to a single Ubuntu VPS (Virtual Private Server) machine running Nginx. This documentation provides instructions on how to build, run, and deploy using the Beads CLI.

## Setup
1. Install Python 3.9
2. Clone the repo
3. Navigate to the project's directory and create a virtualenv using: `python -m venv .venv && source .venv/bin/activate`

## Run
### Source Mode
If you’re developing or testing the CLI, you can run it directly from the source using:
```bash
python -m src.cli {COMMAND} ...
```
This is ideal during development when the CLI is not yet packaged.

### Packaged Mode
Once the CLI is built and bundled, follow these steps to deploy an application:

1. Run `bead init`
2. Run `bead set-host`
3. Get a domain and a docker image you wish to deploy
4. Run `bead deploy` with the domain and image as parameters


## Build
To build the Beads CLI, run the following command in your terminal:
```bash
python setup.py build
```
This will create a bundled version of the CLI tool that can be used as a standalone executable.

## Troubleshooting
The Beads CLI simplifies the process of deploying applications by automating configuration and deployment steps. Make sure to follow the instructions carefully to set up your environment correctly.

Note: Ensure that your VPS and container registry credentials are correctly set up before running the bead deploy command to avoid any authentication issues.
