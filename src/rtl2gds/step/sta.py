import logging
import os
import subprocess

from rtl2gds.global_configs import DEFAULT_SDC_FILE, ENV_TOOLS_PATH, StepName
from rtl2gds.step.configs import SHELL_CMD


def run(
    top_name: str,
    input_def: str,
    result_dir: str,
    clk_port_name: str,
    clk_freq_mhz: float,
    sta_report_dirname: str = "sta",
):
    assert os.path.exists(input_def)

    artifacts = {"sta_report_dir": f"{result_dir}/{sta_report_dirname}"}

    shell_env = {
        "TOP_NAME": top_name,
        "INPUT_DEF": input_def,
        "RESULT_DIR": result_dir,
        "SDC_FILE": DEFAULT_SDC_FILE,
        "CLK_PORT_NAME": clk_port_name,
        "CLK_FREQ_MHZ": str(clk_freq_mhz),
        "TOOL_REPORT_DIR": artifacts["sta_report_dir"],
    }

    shell_cmd = SHELL_CMD[StepName.STA]
    logging.info(
        "(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
        StepName.STA,
        str(shell_cmd),
        str(shell_env),
    )

    shell_env.update(ENV_TOOLS_PATH)

    ret_code = subprocess.call(shell_cmd, env=shell_env)
    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, shell_cmd)

    # iterate through artifacts and check if they exist
    for key, value in artifacts.items():
        if not os.path.exists(value):
            raise FileNotFoundError(
                f"Step({StepName.STA}) Expected artifact {key} not found: {value}"
            )

    metrics = {}
    return metrics, artifacts


if __name__ == "__main__":
    # Example usage

    top_name = "picorv32a"
    result_dir = "."
    sta_report_dirname = "sta_report"
    def_file = "/opt/rtl2gds/design_zoo/picorv32a/pico_results/picorv32a_cts.def"
    _, sta_res_files = run(
        top_name, def_file, result_dir, "clk", 100, sta_report_dirname
    )
