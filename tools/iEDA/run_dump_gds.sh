set -e

# (fixed) iEDA setting
PWD=$(cd "$(dirname "$0")";pwd)
export CONFIG_DIR=${PWD}/iEDA_config
export TCL_SCRIPT_DIR=${PWD}/script

# export DEF_FILE=
# export GDS_FILE=

iEDA -script "${TCL_SCRIPT_DIR}/DB_script/run_def_to_gds_var.tcl"
