# necessary directories
DESIGN_PATH=${PROJ_PATH}/aes
export RESULT_DIR="${DESIGN_PATH}/results"

# design settings
export DESIGN_TOP="aes_cipher_top"
export RTL_FILE="${DESIGN_PATH}/aes_cipher_top.v
${DESIGN_PATH}/aes_inv_cipher_top.v
${DESIGN_PATH}/aes_inv_sbox.v
${DESIGN_PATH}/aes_key_expand_128.v
${DESIGN_PATH}/aes_rcon.v
${DESIGN_PATH}/aes_sbox.v
${DESIGN_PATH}/timescale.v"
export NETLIST_FILE="${NETLIST_DIR}/aes_netlist.v"

# design constrains
export CLK_FREQ_MHZ=100
export CLK_PORT_NAME="clk"
export DIE_AREA="0.0 0.0 700 700"
export CORE_AREA="10 10 690 690"
