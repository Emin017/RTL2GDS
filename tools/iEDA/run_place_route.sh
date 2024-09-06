set -e

# (fixed) iEDA setting
PWD=$(cd "$(dirname "$0")";pwd)
export CONFIG_DIR=${PWD}/iEDA_config
export TCL_SCRIPT_DIR=${PWD}/script

TCL_SCRIPTS="iNO_script/run_iNO_fix_fanout.tcl
iPL_script/run_iPL.tcl
iCTS_script/run_iCTS.tcl
iCTS_script/run_iCTS_STA.tcl
iTO_script/run_iTO_drv.tcl
iTO_script/run_iTO_drv_STA.tcl
iTO_script/run_iTO_hold.tcl
iTO_script/run_iTO_hold_STA.tcl
iPL_script/run_iPL_legalization.tcl
iRT_script/run_iRT.tcl
iPL_script/run_iPL_filler.tcl
DB_script/run_def_to_gds_text.tcl"
# DB_script/run_def_to_json_text.tcl
# iRT_script/run_iRT_DRC.tcl

for SCRIPT in $TCL_SCRIPTS; do
    echo ">>> $ iEDA -script ${TCL_SCRIPT_DIR}/${SCRIPT}"
    iEDA -script "${TCL_SCRIPT_DIR}/${SCRIPT}"
done
