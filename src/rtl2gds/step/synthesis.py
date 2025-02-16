"""
Synthesis step implementation using yosys
"""

import logging
import math
import os
import subprocess
from typing import List, Optional, Union

from ..global_configs import ENV_TOOLS_PATH
from .configs import SHELL_CMD

MAX_CELL_AREA = 1_000_000
STEP_NAME = __file__.rsplit("/", maxsplit=1)[-1].split(".")[0]


def get_yosys_top_info(report_path: str):
    """Extract top module area and name from yosys report"""
    found_top_summary = False

    with open(report_path, "r", encoding="utf-8") as file:
        for line in file:
            if "=== design hierarchy ===" in line:
                found_top_summary = True
            if found_top_summary and "Chip area for top module" in line:
                # Extract the top name and area from the line
                parts = line.split(":")
                top_name = parts[0].split("'\\")[-1].strip("': ")
                cell_area = float(parts[1].strip())
                return cell_area, top_name

    assert False, "Top module information not found in the report"


def run(
    design_top: str,
    rtl_file: Union[str, List[str]],
    netlist_file: str,
    sdc_file: str,
    result_dir: str,
    clk_port_name: str,
    clk_freq_mhz: str,
    die_area: Optional[str] = None,
    core_area: Optional[str] = None,
    core_util: Optional[float] = None,
):
    """
    Run synthesis step using yosys

    Args:

    Returns:
        dict: Updated environment variables

    Raises:
        subprocess.CalledProcessError: If synthesis fails
        AssertionError: If required parameters are missing
    """
    assert os.path.exists(rtl_file)
    if isinstance(rtl_file, list):
        rtl_file = " \n ".join(rtl_file)

    step_cmd = SHELL_CMD[STEP_NAME]

    yosys_report_dir = f"{result_dir}/yosys"
    os.makedirs(yosys_report_dir, exist_ok=True)

    step_env = {
        "DESIGN_TOP": str(design_top),
        "RTL_FILE": str(rtl_file),
        "NETLIST_FILE": str(netlist_file),
        "SDC_FILE": str(sdc_file),
        "YOSYS_REPORT_DIR": str(yosys_report_dir),
        "CLK_PORT_NAME": str(clk_port_name),
        "CLK_FREQ_MHZ": str(clk_freq_mhz),
    }

    if die_area and core_area:
        step_env.update(
            {
                "DIE_AREA": str(die_area),
                "CORE_AREA": str(core_area),
            }
        )
    elif core_util:
        assert 0 < core_util < 1, f"Core utilization {core_util} out of range (0,1)"
        step_env.update(
            {
                "CORE_UTIL": str(core_util),
            }
        )

    else:
        assert (
            core_util is not None
        ), "Either die_area/core_area or core_util must be provided"

    logging.info(
        "(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
        STEP_NAME,
        str(step_cmd),
        step_env,
    )

    step_env.update(ENV_TOOLS_PATH)
    ret_code = subprocess.call(step_cmd, env=step_env)
    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, step_cmd)

    synth_stat = f"{yosys_report_dir}/synth_stat.txt"
    assert os.path.exists(synth_stat), "Synthesis statistic file not found"
    assert os.path.exists(netlist_file), "Netlist file not found"

    cell_area, top_name = get_yosys_top_info(synth_stat)
    assert top_name == design_top, "Top module name mismatch"
    assert 0 < cell_area < MAX_CELL_AREA, "Cell area exceeds processing limit"

    # Calculate die and core area if not provided
    if not (die_area and core_area):
        core_length = math.sqrt(cell_area / core_util)
        io_margin = 10
        die_area = f"0 0 {core_length+io_margin*2} {core_length+io_margin*2}"
        core_area = (
            f"{io_margin} {io_margin} {core_length+io_margin} {core_length+io_margin}"
        )

    elif not core_util:
        core = core_area.split(" ")
        core_len_x = float(core[2]) - float(core[0])
        core_len_y = float(core[3]) - float(core[1])
        core_area = core_len_x * core_len_y
        core_util = cell_area / core_area
        assert 0 < core_util < 1, "Core utilization out of range"

    else:
        assert 0

    return {
        "DIE_AREA": die_area,
        "CORE_AREA": core_area,
        "CORE_UTIL": core_util,
    }


# if __name__ == "__main__":
#     logging.basicConfig(
#         format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
#         level=logging.INFO,
#     )

#     logging.info("Testing synthesis...")

#     # Setup test design
#     TEST_DESIGN_TOP = "aes_cipher_top"
#     test_rtl = [
#         "/home/wsl/rtl2gds/design_zoo/aes/aes_cipher_top.v",
#         "/home/wsl/rtl2gds/design_zoo/aes/aes_inv_cipher_top.v",
#         "/home/wsl/rtl2gds/design_zoo/aes/aes_inv_sbox.v",
#         "/home/wsl/rtl2gds/design_zoo/aes/aes_key_expand_128.v",
#         "/home/wsl/rtl2gds/design_zoo/aes/aes_rcon.v",
#         "/home/wsl/rtl2gds/design_zoo/aes/aes_sbox.v",
#         "/home/wsl/rtl2gds/design_zoo/aes/timescale.v",
#     ]
#     RESULT_DIR = "./results"
#     OUTPUT_NETLIST = "./results/aes_netlist.v"

#     import shutil

#     shutil.rmtree(RESULT_DIR)

#     from ..global_configs import DEFAULT_SDC_FILE
#     from ..design_constrain import DesignConstrain
#     from ..design_path import DesignPath

#     path_setting = DesignPath(
#         rtl_file=test_rtl,
#         result_dir=RESULT_DIR,
#         netlist_file=OUTPUT_NETLIST,
#         sdc_file=DEFAULT_SDC_FILE,
#     )
#     constrain = DesignConstrain(clk_port_name="clk", clk_freq_mhz="100", core_util=0.5)

#     env = run(
#         design_top=TEST_DESIGN_TOP, design_path=path_setting, design_constrain=constrain
#     )

#     logging.info("Synthesis completed successfully")
#     logging.info("Generated netlist: %s", env["NETLIST_FILE"])
#     logging.info("Die area: %s", env["DIE_AREA"])
#     logging.info("Core area: %s", env["CORE_AREA"])
#     logging.info("env: %s", env)
