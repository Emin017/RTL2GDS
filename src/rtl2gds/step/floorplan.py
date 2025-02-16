"""
Floorplan step implementation using iEDA-iFP
"""

import json
import logging
import subprocess

from ..global_configs import ENV_TOOLS_PATH, StepName
from .configs import SHELL_CMD

STEP_NAME = StepName.FLOORPLAN


def run(
    design_top: str,
    result_dir: str,
    sdc_file: str,
    input_netlist: str,
    output_def: str,
    die_area: str,
    core_area: str,
) -> dict:
    """
    Run floorplan step using iEDA-iFP.

    Args:
        design_path (DesignPath): Design paths including netlist and DEF files
        design_constrain (DesignConstrain): Design timing and area constraints

    Returns:
        dict: Updated environment variables

    Raises:
        subprocess.CalledProcessError: If floorplan fails
    """
    step_cmd = SHELL_CMD[STEP_NAME]

    # Prepare environment variables
    step_env = {
        "DESIGN_TOP": design_top,
        "RESULT_DIR": result_dir,
        "SDC_FILE": sdc_file,
        "NETLIST_FILE": input_netlist,
        "OUTPUT_DEF": output_def,
        "DIE_AREA": die_area,
        "CORE_AREA": core_area,
    }

    logging.info(
        "(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
        STEP_NAME,
        str(step_cmd),
        str(step_env),
    )

    step_env.update(ENV_TOOLS_PATH)
    ret_code = subprocess.call(step_cmd, env=step_env)
    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, step_cmd)

    # collect results
    layout_summary_json = f"{result_dir}/feature/summary_{STEP_NAME}.json"
    with open(
        layout_summary_json,
        "r",
        encoding="utf-8",
    ) as f:
        summary = json.load(f)
        die_width = float(summary["Design Layout"]["die_bounding_width"])
        die_height = float(summary["Design Layout"]["die_bounding_height"])
        core_width = float(summary["Design Layout"]["core_bounding_width"])
        core_height = float(summary["Design Layout"]["core_bounding_height"])
        core_util = float(summary["Design Layout"]["core_usage"])

        margin_width = float(die_width - core_width)/2
        margin_height = float(die_height - core_height)/2

        # @TODO: collect core_shape from summary.json
        # core_bottom_left_x = summary["Design Layout"]["core_bot_left_x"]
        # core_bottom_left_y = summary["Design Layout"]["core_bot_left_y"]
        # core_top_right_x = summary["Design Layout"]["core_top_right_x"]
        # core_top_right_y = summary["Design Layout"]["core_top_right_y"]

    return dict(
        {
            "DIE_AREA": f"0 0 {die_width} {die_height}",
            "CORE_AREA": f"{margin_width} {margin_height} {margin_width+core_width} {margin_height+core_height}",
            "CORE_UTIL": core_util,
        }
    )


# if __name__ == "__main__":
#     logging.basicConfig(
#         format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
#         level=logging.INFO,
#     )

#     logging.info("Testing floorplan...")

#     # Setup test design
#     TEST_DESIGN_TOP = "aes_cipher_top"
#     RESULT_DIR = "./results"
#     INPUT_NETLIST = "./results/aes_netlist.v"
#     OUTPUT_DEF = "./results/aes_fp.def"

#     from ..design_constrain import DesignConstrain
#     from ..design_path import DesignPath
#     from ..global_configs import DEFAULT_SDC_FILE

#     test_path = DesignPath(
#         rtl_file="",
#         sdc_file=DEFAULT_SDC_FILE,
#         netlist_file=INPUT_NETLIST,
#         def_file=OUTPUT_DEF,
#         result_dir=RESULT_DIR,
#     )

#     test_constrain = DesignConstrain(
#         clk_port_name="",
#         clk_freq_mhz="",
#         die_area="0 0 700 700",
#         core_area="10 10 690 690",
#     )

#     env = run(
#         design_top=TEST_DESIGN_TOP,
#         design_path=test_path,
#         design_constrain=test_constrain,
#     )

#     import os

#     assert os.path.exists(OUTPUT_DEF)
#     logging.info("Generated def: %s", env["OUTPUT_DEF"])
#     logging.info("env: %s", env)
