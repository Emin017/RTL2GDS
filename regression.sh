#!/usr/bin/env bash
set -e
export PROJ_PATH=$(cd "$(dirname "$0")";pwd)

BINARY_PATH="${PROJ_PATH}/bin"
source ${BINARY_PATH}/runtime_env_setup.sh

# preprocess
export FOUNDRY_DIR="${PROJ_PATH}/foundry/sky130"
test -e ${FOUNDRY_DIR}/lib/merged.lib || bash ${FOUNDRY_DIR}/mergelib.sh

# test design
TEST_DESIGNS="gcd
picorv32a
aes"

for DESIGN in $TEST_DESIGNS; do
    source ${PROJ_PATH}/${DESIGN}/config.sh
    rm -rf ${RESULT_DIR}
    mkdir -p ${NETLIST_DIR}
    yosys ${PROJ_PATH}/tools/yosys/yosys.tcl
    bash ${PROJ_PATH}/tools/iEDA/run_floorplan.sh
    bash ${PROJ_PATH}/tools/iEDA/run_place_route.sh
done
