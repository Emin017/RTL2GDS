import os
from dataclasses import dataclass

PKG_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PKG_BIN_DIR = os.path.abspath(PKG_SRC_DIR + "/../../bin")
PKG_PDK_DIR = os.path.abspath(PKG_SRC_DIR + "/../../foundry/sky130")
PKG_TOOL_DIR = os.path.abspath(PKG_SRC_DIR + "/../../tools")

_BIN_ENV = os.environ["PATH"] if "PATH" in os.environ else ""
_LIB_ENV = os.environ["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in os.environ else ""

ENV_TOOLS_PATH = {
    "PATH": f"{PKG_BIN_DIR}/iEDA:{PKG_BIN_DIR}/yosys/bin:{_BIN_ENV}",
    "LD_LIBRARY_PATH": f"{PKG_BIN_DIR}/lib:{_LIB_ENV}",
    "FOUNDRY_DIR": PKG_PDK_DIR,
    "TCL_SCRIPT_DIR": f"{PKG_TOOL_DIR}/iEDA/script",
    "CONFIG_DIR": f"{PKG_TOOL_DIR}/iEDA/iEDA_config",
    "RUST_BACKTRACE": "1",
    "VERILOG_INCLUDE_DIRS": "",
}

DEFAULT_SDC_FILE = f"{PKG_TOOL_DIR}/default.sdc"


# Flow & Step settings
@dataclass
class StepName:
    """RTL2GDS flow step names"""

    RTL2GDS_ALL = "rtl2gds_all"
    INIT = "init"
    SYNTHESIS = "synthesis"
    FLOORPLAN = "floorplan"
    FIXFANOUT = "fixfanout"
    PLACE = "place"
    CTS = "cts"
    DRV_OPT = "drv_opt"
    HOLD_OPT = "hold_opt"
    LEGALIZE = "legalize"
    ROUTE = "route"
    FILLER = "filler"
    LAYOUT_GDS = "dump_layout_gds"
    LAYOUT_JSON = "dump_layout_json"


# Flow step sequences
RTL2GDS_FLOW_STEP = [
    StepName.INIT,
    StepName.SYNTHESIS,
    StepName.FLOORPLAN,
    StepName.FIXFANOUT,
    StepName.PLACE,
    StepName.CTS,
    StepName.DRV_OPT,
    StepName.HOLD_OPT,
    StepName.LEGALIZE,
    StepName.ROUTE,
    StepName.FILLER,
]

PR_FLOW_STEP = RTL2GDS_FLOW_STEP[3:]
