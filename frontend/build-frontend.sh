#!/bin/bash

##
# Optional script for compiling the frontend in a docker container
# Compiles into your local directory (not into the container)
#
# Reasons
#   a) Consistent environment between devs, and between local vs CI/CD
#   b) For use by those who don't have node.js installed locally
#      Especially when wanting to run pulumi up locally
#   c) The above also apply for the Gitlab runner environment
#   d) Having a local script to do this helps in development and debugging of the CI job script
#   e) The work is be reusable as the script of the CI job
#      i.e. `bash ./backend/build-frontend.sh local` instead of writing lines of code
#
# Usage
#   cd ./frontend
#   Local
#     bash build-frontend.sh local # runs npm install and npm run build locally in your terminal
#   Docker
#     bash build-frontend.sh docker # runs npm install and npm run build inside a container (but outputs files to the local directory)
#
# Requirements
#   docker
##

DOCKER_IMAGE="node:18-alpine3.17"
ENVIRONMENT=${ENVIRONMENT:-develop}

# Source the develop variable by default. Override if necessary using ENVIRONMENT=xyz bash build-frontend.sh
source .env.${ENVIRONMENT}

# Mount the  directory in the docker container
# and run the compile commands
# Docker 'run' command reference: https://docs.docker.com/engine/reference/commandline/run/
command_docker="
docker run \
  -v $(pwd):/rasd \
  --workdir /rasd
  -e VITE_API_BASE_URL=${VITE_API_BASE_URL:?Not set!}
  -e ENVIRONMENT=${ENVIRONMENT}
  ${DOCKER_IMAGE}
"

# The general command that will run either locally or inside the container
# note that the CI script uses npm run build -- --mode $CI_COMMIT_BRANCH
# We don't have that variable, so we pass the value directly to the container environment (above)
command_general="
  npm install && \
  npm run build -- --mode $ENVIRONMENT
"

# check if we have been told to run in docker (default)
# or local
echo "$0: Received arg: ${1:-"No arg. defaulting to 'docker'"}"
if [[ "${1:-docker}" == "docker" ]]; then
  command="$command_docker $command_general"
fi
if [[ "$1" == "local" ]]; then
  command=$command_general
fi

1>&2 echo "$0: running command: $command"
eval $command
