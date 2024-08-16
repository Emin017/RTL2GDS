#!/usr/bin/env bash
set -e
export PROJ_PATH=$(cd "$(dirname "$0")";pwd)
BINARY_PATH="${PROJ_PATH}/bin"
source ${BINARY_PATH}/runtime_env_setup.sh

# please change your design config
source ${PROJ_PATH}/picorv32a/config.sh

# preprocess
test -e $FOUNDRY_DIR/lib/merged.lib || bash $FOUNDRY_DIR/mergelib.sh
mkdir -p $RESULT_DIR/verilog

# run synthesis
yosys ${PROJ_PATH}/tools/yosys/yosys.tcl

# run floorplan
bash ${PROJ_PATH}/tools/iEDA/run_floorplan.sh

# run placement and routing
bash ${PROJ_PATH}/tools/iEDA/run_place_route.sh
