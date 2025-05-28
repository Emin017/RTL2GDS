#===========================================================
##   init flow config
#===========================================================
flow_init -config $IEDA_CONFIG_DIR/flow_config.json

#===========================================================
##   read db config
#===========================================================
db_init -config $IEDA_CONFIG_DIR/db_default_config.json -output_dir_path $RESULT_DIR

tech_lef_init
lef_init

#===========================================================
##   read def
#===========================================================
def_init -path $::env(INPUT_DEF)

lef_save -path $::env(ABSTRACT_LEF_FILE)


#flow_exit
