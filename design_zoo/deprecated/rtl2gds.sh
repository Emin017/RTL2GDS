#!/usr/bin/env bash
set -e
# should move to $PROJ_PATH base directory
export PROJ_PATH=$(cd "$(dirname "$0")";pwd)
export SDC_FILE="${PROJ_PATH}/tools/default.sdc"
export FOUNDRY_DIR="${PROJ_PATH}/foundry/sky130"
BINARY_PATH="${PROJ_PATH}/bin"
source ${BINARY_PATH}/runtime_env_setup.sh

# please change your design config.sh file
source ${PROJ_PATH}/design_zoo/gcd/gcd_config.sh

# preprocess
test -e $FOUNDRY_DIR/lib/merged.lib || bash $FOUNDRY_DIR/mergelib.sh
mkdir -p $RESULT_DIR/yosys

# run synthesis
yosys ${PROJ_PATH}/tools/yosys/yosys.tcl

# run floorplan
bash ${PROJ_PATH}/tools/iEDA/run_floorplan.sh

# run placement and routing
bash ${PROJ_PATH}/tools/iEDA/run_place_route.sh
