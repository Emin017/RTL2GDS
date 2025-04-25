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
##   read lef
#===========================================================
source $IEDA_TCL_SCRIPT_DIR/DB_script/db_init_lef.tcl

#===========================================================
##   read def
#===========================================================
def_init -path $RESULT_DIR/iRT_result.def

#===========================================================
##   run DRC and save result
#===========================================================
run_drc -config $IEDA_CONFIG_DIR/drc_default_config.json -path $RESULT_DIR/report/drc/iRT_drc.rpt
save_drc -path $RESULT_DIR/drc/detail.drc

#read_drc -path $RESULT_DIR/drc/detail.drc

#===========================================================
##   Exit 
#===========================================================
flow_exit
