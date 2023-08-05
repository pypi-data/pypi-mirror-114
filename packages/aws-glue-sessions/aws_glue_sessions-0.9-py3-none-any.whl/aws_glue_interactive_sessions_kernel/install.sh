#!/bin/bash

# Move kernels to shared folder
SYSTEM_PYTHON_PREFIX=$(python3 -c "from __future__ import print_function;import sys; print(sys.prefix)")
shared_juptyer_path="${SYSTEM_PYTHON_PREFIX}/share/jupyter/kernels"
mkdir -p ${shared_juptyer_path}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cp -a "${DIR}/glue_python_kernel" "${shared_juptyer_path}/"
cp -a "${DIR}/glue_scala_kernel" "${shared_juptyer_path}/"
cp -a "${DIR}/glue_kernel_utils" "${shared_juptyer_path}/"
# enable jupyter widgets
#jupyter nbextension enable --py widgetsnbextension
#jupyter labextension install @jupyter-widgets/jupyterlab-manager
# update service-2.json
aws configure add-model --service-model file://${DIR}/service-2.json --service-name glue

