DESIGN_PATH=${PROJ_PATH}/picorv32a

# necessary directories
export FOUNDRY_DIR="${DESIGN_PATH}/../foundry/sky130"
export RESULT_DIR="${DESIGN_PATH}/results"
export NETLIST_DIR="${RESULT_DIR}/verilog"

# design settings
export DESIGN_TOP="picorv32a"
export RTL_FILE="${DESIGN_PATH}/${DESIGN_TOP}.v"
export SDC_FILE="${DESIGN_PATH}/${DESIGN_TOP}.sdc"
export NETLIST_FILE="${NETLIST_DIR}/${DESIGN_TOP}.v"

# design constrains
export CLK_FREQ_MHZ=100
export CLK_PORT_NAME="clk"
export DIE_AREA="0.0 0.0 900 900"
export CORE_AREA="10 10 890 890"
