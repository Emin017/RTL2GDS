#===========================================================
#   environment variables
#===========================================================
set INPUT_DEF           "$::env(INPUT_DEF)"
set GDS_FILE            "$::env(GDS_FILE)"
set RESULT_DIR          "$::env(RESULT_DIR)"

set IEDA_CONFIG_DIR     "$::env(IEDA_CONFIG_DIR)"
set IEDA_TCL_SCRIPT_DIR "$::env(IEDA_TCL_SCRIPT_DIR)"

if { $INPUT_DEF == "" } {
  set INPUT_DEF "$RESULT_DIR/iPL_filler_result.def"
}
if { $GDS_FILE == "" } {
  set GDS_FILE "$RESULT_DIR/final_design.gds2"
}

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
def_init -path $INPUT_DEF

#===========================================================
##   save gds 
#===========================================================
gds_save -path $GDS_FILE

#===========================================================
##   Exit 
#===========================================================
flow_exit
