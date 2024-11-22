"""
Floorplan step implementation using iEDA-iFP
"""

import logging
import subprocess

from rtl2gds.design_constrain import DesignConstrain
from rtl2gds.design_path import DesignPath
from rtl2gds.global_configs import ENV_TOOLS_PATH
from rtl2gds.step.configs import SHELL_CMD


def run(
    design_top: str,
    design_path: DesignPath,
    design_constrain: DesignConstrain,
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
    step_name = __file__.rsplit("/", maxsplit=1)[-1].split(".")[0]
    step_cmd = SHELL_CMD[step_name]

    # Prepare environment variables
    step_env = {
        "DESIGN_TOP": design_top,
        "RESULT_DIR": design_path.result_dir,
        "SDC_FILE": design_path.sdc_file,
        "NETLIST_FILE": design_path.netlist_file,
        "OUTPUT_DEF": design_path.def_file,
        "DIE_AREA": design_constrain.die_area,
        "CORE_AREA": design_constrain.core_area,
    }

    logging.info(
        "(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
        step_name,
        str(step_cmd),
        str(step_env),
    )

    step_env.update(ENV_TOOLS_PATH)
    ret_code = subprocess.call(step_cmd, env=step_env)
    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, step_cmd)

    return step_env


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
        level=logging.INFO,
    )

    logging.info("Testing floorplan...")

    # Setup test design
    TEST_DESIGN_TOP = "aes_cipher_top"
    RESULT_DIR = "./results"
    INPUT_NETLIST = "./results/aes_netlist.v"
    OUTPUT_DEF = "./results/aes_fp.def"

    from rtl2gds.global_configs import DEFAULT_SDC_FILE

    test_path = DesignPath(
        rtl_file="",
        sdc_file=DEFAULT_SDC_FILE,
        netlist_file=INPUT_NETLIST,
        def_file=OUTPUT_DEF,
        result_dir=RESULT_DIR,
    )

    test_constrain = DesignConstrain(
        clk_port_name="",
        clk_freq_mhz="",
        die_area="0 0 700 700",
        core_area="10 10 690 690",
    )

    env = run(
        design_top=TEST_DESIGN_TOP,
        design_path=test_path,
        design_constrain=test_constrain,
    )

    import os

    assert os.path.exists(OUTPUT_DEF)
    logging.info("Generated def: %s", env["OUTPUT_DEF"])
    logging.info("env: %s", env)
