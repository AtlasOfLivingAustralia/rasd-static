#!/bin/bash

##
# Runs a few basic tests
# Intended to run after a deployment, to verify that it succeeded and didn't break anything
##

echo "$0: Start of script."

##
# Set values

unset fail
err=0
# Check if root_url is passed as an argument
if [[ -z "$1" ]]; then
    echo "❌ Error: root_url is required as an argument."
    echo "Usage: $0 <root_url>"
    exit 1
fi

# Set root_url from the first argument
root_url=$1
api_suffix="/v1/"

# Unfortunately, apparently Macs don't come with Bash 4 which is the minimum to support hash tables (dictionaries)
# declare -A endpoints
# endpoints["root"]="301"
# endpoints["docs"]="200"
# endpoints["health"]="405"

endpoints=(
  "root" # gets translated to "" i.e. /
  "docs"
  "health"
)

# Define desired return codes for each endpoint
root="307"    # /
docs="200"    # /api/v1/docs
health="204"  # /api/v1/health

# Normally we'd use -I for 'HEAD' but Hayden didn't implement the backend that way.
curl_prefix='curl -s -o /dev/null -w "%{http_code}"'

##
# Test endpoints
for endpoint in "${endpoints[@]}"; do

  temp_suffix=$api_suffix
  desired_result="${!endpoint}"

  # Fix root
  if [[ $endpoint == "root" ]]; then
    endpoint=""
    temp_suffix=""
  fi

  url="$root_url$temp_suffix$endpoint"

  command="$curl_prefix $url"

  echo "Testing for $desired_result from $url"
  echo "running command: $command"

  # Run command and check result
  actual_result="$(eval $command)"
  if [[ "$desired_result" == "$actual_result" ]]; then
    echo "---> Pass"
  else
    echo "---> Fail (got $actual_result)"
    fail="TRUE"
  fi

done

##
# Print overall result
if [[ -n "$fail" ]]; then
  echo "$0: One or more tests failed."
  err=1
else
  echo "$0: All tests passed."
fi

# End of script
echo "$0: End of script."
exit $err