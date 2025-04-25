import logging
import subprocess

from ..global_configs import R2G_PDK_DIR_IHP130, R2G_TOOL_DIR, StepName

STEP_NAME = StepName.DRC

def run(top_name: str, gds_file: str, result_dir: str, tool: str = "magic"):
    """
    Run DRC check using the specified tool.
    
    Args:
        top_name (str): Top module name.
        gds_file (str): Path to the input GDS file.
        result_dir (str): Directory to store results.
        tool (str): Tool to use for DRC. Default is "magic".
    
    Returns:
        tuple: Metrics and artifacts from the DRC run.
    """
    if tool == "magic":
        return drc_magic(top_name, gds_file, result_dir)
    else:
        return drc_klayout(top_name, gds_file, result_dir)
def drc_magic(top_name: str, gds_file: str, result_dir: str):
    
    artifacts = {
        "drc_report_text": f"{result_dir}/report/drc_magic.txt",
        "drc_report_mag": f"{result_dir}/report/drc_magic.mag",
    }

    shell_cmd = [
        "magic",
        "-noconsole",
        "-dnull",
        "-rcfile",
        f"{R2G_PDK_DIR_IHP130}/ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc",
        f"{R2G_TOOL_DIR}/magic/magic_drc.tcl", # @TODO
        gds_file,
        top_name,
        f"{R2G_PDK_DIR_IHP130}",
        f"{result_dir}/drc_magic.txt",
        f"{result_dir}/drc_magic.mag",
    ]

    logging.info(
        "(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
        STEP_NAME,
        str(shell_cmd),
    )

    ret_code = subprocess.call(shell_cmd)
    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, shell_cmd)

    metrics = {}

    return metrics, artifacts


def drc_klayout(top_name: str, gds_file: str, result_dir: str):
    """
    Run DRC check using KLayout.
    
    Args:
        top_name (str): Top module name.
        gds_file (str): Path to the input GDS file.
        result_dir (str): Directory to store results.
    
    Returns:
        tuple: Metrics and artifacts from the DRC run.
    """
    # Placeholder for KLayout DRC implementation
    raise NotImplementedError("KLayout DRC is not implemented yet.")

if __name__ == "__main__":
    # Example usage
    top_name = "tt_um_kianV_rv32ima_uLinux_SoC"
    gds_file = f"/home/user/demo/kianvconfigs/orfs/results/ihp-sg13g2/kianv/base/6_final.gds"
    result_dir = "./result"

    _, drc_res_files = run(top_name, gds_file, result_dir)

    with open(drc_res_files["drc_report_text"], 'r') as f:
        contents = f.read()
        print(contents)
