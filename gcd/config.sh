DESIGN_PATH=${PROJ_PATH}/gcd

# necessary directories
export FOUNDRY_DIR="${DESIGN_PATH}/../foundry/sky130"
export RESULT_DIR="${DESIGN_PATH}/results"
export NETLIST_DIR="${RESULT_DIR}/verilog"

# design settings
export DESIGN_TOP="gcd"
export RTL_FILE="${DESIGN_PATH}/${DESIGN_TOP}.v"
export SDC_FILE="${DESIGN_PATH}/${DESIGN_TOP}.sdc"
export NETLIST_FILE="${NETLIST_DIR}/${DESIGN_TOP}.v"

# design constrains
export CLK_FREQ_MHZ=200
export CLK_PORT_NAME="clk"
export DIE_AREA="0.0 0.0 120 120"
export CORE_AREA="10 10 110 110"
