"""
Dump layout GDS step for RTL2GDS flow.
"""

import logging
import subprocess
from typing import Optional

from klayout import lay

from ..global_configs import DEFAULT_SDC_FILE, ENV_TOOLS_PATH
from .configs import SHELL_CMD


def save_snapshot_image(
    gds_file: str, img_file: str, weight: int = 800, height: int = 800
):
    """
    Takes a screenshot of a GDS file and saves it as an image.
    @Reference: https://gist.github.com/sequoiap/48af5f611cca838bb1ebc3008eef3a6e

    Args:
        gds_file (str): Path to the input GDS file
        img_file (str): Path to the output image file
        weight (int, optional): Image width. Defaults to 800
        height (int, optional): Image height. Defaults to 800
    """
    # Set display configuration options
    lv = lay.LayoutView()
    lv.set_config("background-color", "#ffffff")
    lv.set_config("grid-visible", "false")
    lv.set_config("grid-show-ruler", "false")
    lv.set_config("text-visible", "false")

    # Load the GDS file
    lv.load_layout(gds_file, 0)
    lv.max_hier()

    # Event processing for delayed configuration events
    lv.timer()

    # Save the image
    lv.save_image(img_file, weight, height)


def run(
    input_def: str,
    gds_file: str,
    result_dir: str,
    snapshot_file: Optional[str] = None,
):
    """
    Run the layout GDS dump step.

    Args:
        input_def (str): Input DEF file path
        gds_file (str): Output GDS file path
        snapshot_file (Optional[str], optional): Output snapshot image path. Defaults to None.

    Raises:
        subprocess.CalledProcessError: If the GDS dump command fails
    """
    step_name = __file__.rsplit("/", maxsplit=1)[-1].split(".")[0]
    step_cmd = SHELL_CMD[step_name]

    # artifacts = {
    #     "gds": gds_file,
    #     "snapshot": snapshot_file,
    # }

    # Prepare environment variables
    step_env = {
        "INPUT_DEF": input_def,
        "RESULT_DIR": result_dir,
        "GDS_FILE": gds_file,
        "SDC_FILE": DEFAULT_SDC_FILE,
    }
    step_env.update(ENV_TOOLS_PATH)

    logging.info(
        "(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
        step_name,
        step_cmd,
        step_env,
    )

    # Run GDS dump command
    ret_code = subprocess.call(step_cmd, env=step_env)
    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, step_cmd)

    # Generate snapshot if requested
    if snapshot_file:
        save_snapshot_image(gds_file, snapshot_file)


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
        level=logging.INFO,
    )
    # Example usage
    run(
        input_def="layout.def",
        gds_file="output.gds",
        result_dir="./test_result",
        snapshot_file="snapshot.png",
    )
