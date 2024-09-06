import os

pwd = os.getcwd()
foundry_dir = f'{pwd}/../../foundry/sky130'

tool_path = {
    'FOUNDRY_DIR'   : foundry_dir,
    'TCL_SCRIPT_DIR': f'{pwd}/script',
    'CONFIG_DIR'    : f'{pwd}/iEDA_config',
}

design_path = {
    'NETLIST_FILE'  : f'{pwd}/result/verilog/gcd.v',
    'SDC_FILE'      : f'{foundry_dir}/sdc/gcd.sdc',
    'SPEF_FILE'     : f'{foundry_dir}/spef/gcd.spef',
}

keywords = {'NETLIST_FILE', 'SDC_FILE', 'SPEF_FILE', 'FOUNDRY_DIR', 'TCL_SCRIPT_DIR', 'CONFIG_DIR', 'GDS_JSON_FILE', 'RESULT_DIR', 'DESIGN_TOP', 'RTL_FILE', 'GDS_FILE', 'CLK_PORT_NAME', 'CLK_FREQ_MHZ', 'DIE_AREA', 'CORE_AREA'}


shell_cmd = {
    # 'sv2v':       ['sv2v', f'--incdir={default_vars["FOUNDRY_DIR"]}/verilog', f'--top={default_vars["DESIGN_TOP"]}', f'--write={default_vars["DESIGN_TOP"]}.v', default_vars['RTL_FILE']],
    # 'netlist':    ['echo', '"pass run yosys"'],
    'floorplan':    ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iFP_script/run_iFP.tcl'],
    'fixfanout':    ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iNO_script/run_iNO_fix_fanout.tcl'],
    'place':        ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iPL_script/run_iPL.tcl'],
    'cts':          ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iCTS_script/run_iCTS.tcl'],
    'drv_opt':      ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iTO_script/run_iTO_drv.tcl'],
    'hold_opt':     ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iTO_script/run_iTO_hold.tcl'],
    'legalize':     ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iPL_script/run_iPL_legalization.tcl'],
    'route':        ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/iRT_script/run_iRT.tcl'],
    'layout_gds':   ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/DB_script/run_def_to_gds_text.tcl'],
    'layout_json':  ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/DB_script/run_def_to_json_text.tcl'],
    # 'layout_oasis': ['iEDA', '-script', f'{tool_path['TCL_SCRIPT_DIR']}/DB_script/run_def_to_oasis.tcl'],
    }