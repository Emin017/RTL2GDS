set -e

PWD=$(cd "$(dirname "$0")";pwd)

export CONFIG_DIR=${PWD}/iEDA_config
export TCL_SCRIPT_DIR=${PWD}/script

iEDA -script "${TCL_SCRIPT_DIR}/iFP_script/run_iFP.tcl"

# iEDA def file bug, waiting for update
sed -i 's/\( [^+ ]*\) + NET  +/\1 + NET\1 +/' ${RESULT_DIR}/iFP_result.def
