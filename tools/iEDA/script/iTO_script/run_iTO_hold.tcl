#===========================================================
#   environment variables set by user
#===========================================================
set RESULT_DIR          "./ieda_results"

# input files
set INPUT_DEF           "$RESULT_DIR/iTO_drv_result.def"

# output files
set OUTPUT_DEF          "$RESULT_DIR/iTO_hold_result.def"
set OUTPUT_VERILOG      "$RESULT_DIR/iTO_hold_result.v"
set DESIGN_STAT_TEXT    "$RESULT_DIR/report/hold_stat.rpt"
set DESIGN_STAT_JSON    "$RESULT_DIR/report/hold_stat.json"
set TOOL_METRICS_JSON   "$RESULT_DIR/metric/iTO_hold_metrics.json"

# script path
set IEDA_CONFIG_DIR     "$::env(IEDA_CONFIG_DIR)"
set IEDA_TCL_SCRIPT_DIR "$::env(IEDA_TCL_SCRIPT_DIR)"

#===========================================================
#   environment variables
#===========================================================
source $IEDA_TCL_SCRIPT_DIR/DB_script/env_var_setup.tcl

#===========================================================
##   init flow config
#===========================================================
flow_init -config $IEDA_CONFIG_DIR/flow_config.json

#===========================================================
##   read db config
#===========================================================
db_init -config $IEDA_CONFIG_DIR/db_default_config.json -output_dir_path $RESULT_DIR

#===========================================================
##   reset data path
#===========================================================
source $IEDA_TCL_SCRIPT_DIR/DB_script/db_path_setting.tcl

#===========================================================
##   reset lib
#===========================================================
source $IEDA_TCL_SCRIPT_DIR/DB_script/db_init_lib_hold.tcl

#===========================================================
##   reset sdc
#===========================================================
source $IEDA_TCL_SCRIPT_DIR/DB_script/db_init_sdc.tcl

#===========================================================
##   read lef
#===========================================================
source $IEDA_TCL_SCRIPT_DIR/DB_script/db_init_lef.tcl

#===========================================================
##   read def
#===========================================================
def_init -path $INPUT_DEF

#===========================================================
##   run TO to fix_drv，opt_hold, opt_setup
#===========================================================
run_to_hold -config $IEDA_CONFIG_DIR/to_default_config_hold.json

#===========================================================
##   save def 
#===========================================================
def_save -path $OUTPUT_DEF

#===========================================================
##   save netlist 
#===========================================================
netlist_save -path $OUTPUT_VERILOG -exclude_cell_names {}

#===========================================================
##   report db summary
#===========================================================
report_db -path $DESIGN_STAT_TEXT
feature_summary -path $DESIGN_STAT_JSON -step optHold
feature_tool -path $TOOL_METRICS_JSON -step optHold

#===========================================================
##   Exit 
#===========================================================
flow_exit
