set -e

# necessary directories
export FOUNDRY_DIR="${PROJ_PATH}/foundry/sky130"
export RESULT_DIR="$(pwd)/r2g_results"
export NETLIST_DIR="${RESULT_DIR}/verilog"

# preprocess
test -e $FOUNDRY_DIR/lib/merged.lib || bash $FOUNDRY_DIR/mergelib.sh
mkdir -p $RESULT_DIR/verilog

# design settings
export DESIGN_TOP
export RTL_FILE
export SDC_FILE

# design constrains
export CLK_PORT_NAME
export CLK_FREQ_MHZ
export DIE_AREA
export CORE_AREA

export NETLIST_FILE="${NETLIST_DIR}/${DESIGN_TOP}.v"
export GDS_FILE

if [ $RUN_SYNTHESIS != 0 ]; then
    # run synthesis
    yosys ${PROJ_PATH}/tools/yosys/yosys.tcl
fi


if [ $RUN_FLOORPLAN != 0 ]; then
    # run floorplan
    bash ${PROJ_PATH}/tools/iEDA/run_floorplan.sh
fi


if [ $RUN_PLACE_ROUTE != 0 ]; then
    # run placement and routing
    bash ${PROJ_PATH}/tools/iEDA/run_place_route.sh
fi

