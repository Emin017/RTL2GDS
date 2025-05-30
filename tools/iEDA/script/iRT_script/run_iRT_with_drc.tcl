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
def_init -path $RESULT_DIR/iPL_lg_result.def

set temp_folder_path $RESULT_DIR/rt/

init_drc_api

init_rt -temp_directory_path $temp_folder_path \
        -log_level 0 \
        -thread_number 8 \
        -bottom_routing_layer "" \
        -top_routing_layer "" \
        -ra_initial_penalty 100 \
        -ra_penalty_drop_rate 0.8 \
        -ra_outer_max_iter_num 10 \
        -ra_inner_max_iter_num 10

run_rt -flow "dr"

destroy_rt

destroy_drc_api


#===========================================================
##   save def & netlist
#===========================================================
def_save -path $RESULT_DIR/iRT_result.def

#===========================================================
##   save netlist 
#===========================================================
netlist_save -path $RESULT_DIR/iRT_result.v -exclude_cell_names {}

#===========================================================
##   report db summary
#===========================================================
report_db -path "$RESULT_DIR/report/rt_stat.rpt"

#===========================================================
##   Exit 
#===========================================================
flow_exit
