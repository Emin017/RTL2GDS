#!/usr/bin/env bash
set -e
export PROJ_PATH=$(cd "$(dirname "$0")";pwd)
BINARY_PATH="${PROJ_PATH}/bin"
source ${BINARY_PATH}/runtime_env_setup.sh

# please change your design config
source ${PROJ_PATH}/gcd/config.sh

# preprocess
test -e $FOUNDRY_DIR/lib/merged.lib || bash $FOUNDRY_DIR/mergelib.sh
mkdir -p $RESULT_DIR/verilog

# run synthesis
yosys ${PROJ_PATH}/tools/yosys/yosys.tcl

# run floorplan
bash ${PROJ_PATH}/tools/iEDA/run_floorplan.sh

# run placement and routing
bash ${PROJ_PATH}/tools/iEDA/run_place_route.sh

DESIGN_STAGES="iPL_filler_result
iRT_result
iPL_lg_result
iTO_hold_result
iTO_drv_result
iCTS_result
iPL_result
iTO_fix_fanout_result
iFP_result
"

for STAGE in $DESIGN_STAGES; do
    export DEF_FILE=${PROJ_PATH}/r2g_results/${STAGE}.def
    export GDS_FILE=${PROJ_PATH}/r2g_results/${STAGE}.gds
    bash ${PROJ_PATH}/tools/iEDA/run_dump_gds.sh
done
