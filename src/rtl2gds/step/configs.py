"""step shell commands"""

from rtl2gds.global_configs import ENV_TOOLS_PATH, PKG_TOOL_DIR

SHELL_CMD = {
    "synthesis": ["yosys", f"{PKG_TOOL_DIR}/yosys/yosys.tcl"],
    "floorplan": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iFP_script/run_iFP.tcl',
    ],
    "fixfanout": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iNO_script/run_iNO_fix_fanout.tcl',
    ],
    "place": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iPL_script/run_iPL.tcl',
    ],
    "cts": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iCTS_script/run_iCTS.tcl',
    ],
    "drv_opt": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iTO_script/run_iTO_drv.tcl',
    ],
    "hold_opt": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iTO_script/run_iTO_hold.tcl',
    ],
    "legalize": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iPL_script/run_iPL_legalization.tcl',
    ],
    "route": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iRT_script/run_iRT.tcl',
    ],
    "filler": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iPL_script/run_iPL_filler.tcl',
    ],
    "layout_gds": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/DB_script/run_def_to_gds_text.tcl',
    ],
    "dump_layout_json": [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/DB_script/run_def_to_json_text.tcl',
    ],
}


# "sv2v": [
#     "sv2v",
#     f"--incdir={default_vars["FOUNDRY_DIR"]}/verilog",
#     f"--top={default_vars["DESIGN_TOP"]}",
#     f"--write={default_vars["DESIGN_TOP"]}.v",
#     default_vars["RTL_FILE"],
# ]
