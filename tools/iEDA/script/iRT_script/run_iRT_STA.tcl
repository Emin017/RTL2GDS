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
source $IEDA_TCL_SCRIPT_DIR/DB_script/db_init_lib.tcl

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
def_init -path $RESULT_DIR/iRT_result.def

#===========================================================
##   run STA
#===========================================================
init_sta -output $RESULT_DIR/rt/sta/

init_rt -temp_directory_path "$RESULT_DIR/rt/" \
        -bottom_routing_layer "met1" \
        -top_routing_layer "met4" \
        -enable_timing 1

# run_rt -flow vr
run_rt

report_timing -stage "dr"

destroy_rt

#===========================================================
##   Exit 
#===========================================================
flow_exit
