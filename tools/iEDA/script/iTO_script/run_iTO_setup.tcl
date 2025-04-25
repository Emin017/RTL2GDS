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
source $IEDA_TCL_SCRIPT_DIR/DB_script/db_init_lib_setup.tcl

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
def_init -path $RESULT_DIR/iTO_hold_result.def

#===========================================================
##   run TO to  opt_setup
#===========================================================
run_to_setup -config $IEDA_CONFIG_DIR/to_default_config_setup.json

feature_tool -path $RESULT_DIR/feature/ito_optsetup.json -step optSetup


#===========================================================
##   save def 
#===========================================================
def_save -path $RESULT_DIR/iTO_setup_result.def

#===========================================================
##   save netlist 
#===========================================================
netlist_save -path $RESULT_DIR/iTO_setup_result.v -exclude_cell_names {}

#===========================================================
##   report db summary
#===========================================================
report_db -path "$RESULT_DIR/report/setup_stat.rpt"
feature_summary -path $RESULT_DIR/feature/summary_ito_optsetup.json -step optSetup
#===========================================================
##   Exit 
#===========================================================
flow_exit
