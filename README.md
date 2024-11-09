# Run
Run the command `python -m src.cli {COMMAND} ...` to use the CLI during development.

# Usage
## Existing Flow (Django Apps)

### DNS
1. Head to the [hosting provider](https://dcc.godaddy.com/control/portfolio/codelexis.com/settings?itc=mya_vh_buildwebsite_domain) and add an "A record", with a unique subdomain

### Project
1. Add the fully qualified domain name to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in the project's settings.py

### CI Pipeline
1. Point the GitHub workflow files to the new container registry
1. In GitHub, update the `ACR_USERNAME` and `ACR_PASSWORD` secrets to match the ones of the new container registry

### Server
1. Run the script to create a Bead on the server
1. Put an SSL certificate on the domain

### CI Pipeline
1. In the build workflow file, modify the `deploy` job to update the image tag in the target Docker Compose file and restart the machine
1. Also, add the secrets the CI pipeline needs to access the VPS


## New Flow (Any app)
1. Run `bead init`
2. Run `bead set-host`
3. Grab a build for the bead
    - Point the GitHub workflow files to the new container registry
    - In the repository on GitHub, update the `ACR_USERNAME` and `ACR_PASSWORD` secrets to match the ones of the new container registry
    - Trigger a pipeline run and grab the image and tag
4. Run `bead deploy` with the image as a parameter
