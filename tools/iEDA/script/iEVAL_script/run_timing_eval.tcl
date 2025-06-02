idb_init -config $::env(CONFIG_FILE)
source $::env(TCL_SCRIPT_DIR)/DB_script/db_path_setting.tcl
run_timing_eval -eval_output_path $::env(OUTPUT_DIR_PATH) -routing_type $::env(ROUTING_TYPE)