# necessary directories
DESIGN_PATH=${PROJ_PATH}/gcd
export RESULT_DIR="${DESIGN_PATH}/results"

# design settings
export DESIGN_TOP="gcd"
export RTL_FILE="${DESIGN_PATH}/${DESIGN_TOP}.v"
export NETLIST_FILE="${RESULT_DIR}/${DESIGN_TOP}_netlist.v"

# design constrains
export CLK_FREQ_MHZ=200
export CLK_PORT_NAME="clk"
export DIE_AREA="0.0 0.0 120 120"
export CORE_AREA="10 10 110 110"
