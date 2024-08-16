DESIGN_PATH=${PROJ_PATH}/aes

# necessary directories
export FOUNDRY_DIR="${DESIGN_PATH}/../foundry/sky130"
export RESULT_DIR="${DESIGN_PATH}/results"
export NETLIST_DIR="${RESULT_DIR}/verilog"

# design settings
export DESIGN_TOP="aes_cipher_top"
export RTL_FILE="${DESIGN_PATH}/aes_cipher_top.v
${DESIGN_PATH}/aes_inv_cipher_top.v
${DESIGN_PATH}/aes_inv_sbox.v
${DESIGN_PATH}/aes_key_expand_128.v
${DESIGN_PATH}/aes_rcon.v
${DESIGN_PATH}/aes_sbox.v
${DESIGN_PATH}/timescale.v"
export SDC_FILE="${DESIGN_PATH}/aes.sdc"
export NETLIST_FILE="${NETLIST_DIR}/${DESIGN_TOP}.v"

# design constrains
export CLK_FREQ_MHZ=100
export CLK_PORT_NAME="clk"
export DIE_AREA="0.0 0.0 700 700"
export CORE_AREA="10 10 690 690"
