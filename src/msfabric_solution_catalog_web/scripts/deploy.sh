#!/bin/bash
#
#
#       Deploys the web client to Azure Storage Static Website hosting.   
#
# ---------------------------------------------------------------------------------------
#
set -euo pipefail

[ -z "${WEBSITE_STORAGE_CONN_STRING:-}" ] && echo "Error: WEBSITE_STORAGE_CONN_STRING is not set or empty" >&2 && exit 1

GIT_ROOT=$(git rev-parse --show-toplevel)

az storage blob delete-batch -s '$web' --connection-string "$WEBSITE_STORAGE_CONN_STRING"
az storage blob upload-batch -d '$web' -s "${GIT_ROOT}/src/msfabric_solution_catalog_web/out" --connection-string "$WEBSITE_STORAGE_CONN_STRING"

echo "Deployment complete - the site will be live at"
echo
echo "- https://catalogfabric.z9.web.core.windows.net : Right now"
echo "- https://dcnsakthi.github.io/msfabric-solution-catalog          : After DNS cache propagation (GitHub Pages)"
echo


