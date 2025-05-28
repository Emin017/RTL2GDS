"""step shell commands"""

from rtl2gds.global_configs import ENV_TOOLS_PATH, R2G_TOOL_DIR, StepName

SHELL_CMD = {
    StepName.SYNTHESIS: ["yosys", f"{R2G_TOOL_DIR}/yosys/scripts/yosys_synthesis.tcl"],
    StepName.FLOORPLAN: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iFP_script/run_iFP.tcl',
    ],
    StepName.NETLIST_OPT: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iNO_script/run_iNO_fix_fanout.tcl',
    ],
    StepName.PLACEMENT: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iPL_script/run_iPL.tcl',
    ],
    StepName.CTS: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iCTS_script/run_iCTS.tcl',
    ],
    StepName.LEGALIZATION: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iPL_script/run_iPL_legalization.tcl',
    ],
    StepName.ROUTING: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iRT_script/run_iRT.tcl',
    ],
    StepName.FILLER: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iPL_script/run_iPL_filler.tcl',
    ],
    StepName.LAYOUT_GDS: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/DB_script/run_def_to_gds_text.tcl',
    ],
    StepName.LAYOUT_JSON: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/DB_script/run_def_to_json_text.tcl',
    ],
    StepName.STA: [
        "iEDA",
        "-script",
        f'{ENV_TOOLS_PATH["IEDA_TCL_SCRIPT_DIR"]}/iSTA_script/run_iSTA.tcl',
    ],
}
