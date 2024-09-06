# necessary directories
DESIGN_PATH=${PROJ_PATH}/picorv32a
export RESULT_DIR="${DESIGN_PATH}/results"

# design settings
export DESIGN_TOP="picorv32a"
export RTL_FILE="${DESIGN_PATH}/${DESIGN_TOP}.v"
export NETLIST_FILE="${RESULT_DIR}/${DESIGN_TOP}_netlist.v"

# design constrains
export CLK_FREQ_MHZ=100
export CLK_PORT_NAME="clk"
export DIE_AREA="0.0 0.0 900 900"
export CORE_AREA="10 10 890 890"
