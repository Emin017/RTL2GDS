import os

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
RTL2GDS_FLOW_STEP = [
    "synthesis",
    "floorplan",
    "fixfanout",
    "place",
    "cts",
    "drv_opt",
    "hold_opt",
    "legalize",
    "route",
    "filler",
    "layout_gds",
]

PR_FLOW_STEP = RTL2GDS_FLOW_STEP[2:-1]

INIT_STEP = "init"


def main():
    """print all"""
    print(
        "DEFAULT_SDC_FILE:",
        ENV_TOOLS_PATH,
        "\nPKG_SRC_DIR:",
        DEFAULT_SDC_FILE,
        "\nRTL2GDS_FLOW_STEP:",
        RTL2GDS_FLOW_STEP,
        "\nPR_FLOW_STEP:",
        PR_FLOW_STEP,
        "\nINIT_STEP:",
        INIT_STEP,
    )


if __name__ == "__main__":
    main()
