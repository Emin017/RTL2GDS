"""step shell commands"""

from rtl2gds.global_configs import ENV_TOOLS_PATH, PKG_TOOL_DIR, StepName

SHELL_CMD = {
    StepName.SYNTHESIS: ["yosys", f"{PKG_TOOL_DIR}/yosys/yosys.tcl"],
    StepName.FLOORPLAN: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iFP_script/run_iFP.tcl',
    ],
    StepName.FIXFANOUT: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iNO_script/run_iNO_fix_fanout.tcl',
    ],
    StepName.PLACE: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iPL_script/run_iPL.tcl',
    ],
    StepName.CTS: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iCTS_script/run_iCTS.tcl',
    ],
    StepName.DRV_OPT: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iTO_script/run_iTO_drv.tcl',
    ],
    StepName.HOLD_OPT: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iTO_script/run_iTO_hold.tcl',
    ],
    StepName.LEGALIZE: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iPL_script/run_iPL_legalization.tcl',
    ],
    StepName.ROUTE: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iRT_script/run_iRT.tcl',
    ],
    StepName.FILLER: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/iPL_script/run_iPL_filler.tcl',
    ],
    StepName.LAYOUT_GDS: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["TCL_SCRIPT_DIR"]}/DB_script/run_def_to_gds_text.tcl',
    ],
    StepName.LAYOUT_JSON: [
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
