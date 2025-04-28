import json
import logging
import subprocess
import time

import klayout.rdb

from rtl2gds.global_configs import R2G_PDK_DIR_IHP130, R2G_TOOL_DIR, StepName

STEP_NAME = StepName.DRC

def run(top_name: str, gds_file: str, result_dir: str, tool: str = "klayout"):
    """
    Run DRC check using the specified tool.
    
    Args:
        top_name (str): Top module name.
        gds_file (str): Path to the input GDS file.
        result_dir (str): Directory to store results.
        tool (str): Tool to use for DRC. Default is "klayout".
    
    Returns:
        tuple: Metrics and artifacts from the DRC run.
    """
    if tool == "magic":
        return drc_magic(top_name, gds_file, result_dir)
    elif tool == "klayout":
        return drc_klayout(top_name, gds_file, result_dir)
    else:
        raise ValueError(f"Unsupported DRC tool: {tool}")
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


def drc_klayout(
        top_name: str,
        gds_file: str,
        result_dir: str,
        drc_rule_set: str = "sg13g2_minimal"
    ):
    """
    Run DRC check using KLayout.
    
    Args:
        top_name (str): Top module name.
        gds_file (str): Path to the input GDS file.
        result_dir (str): Directory to store results.
        drc_rule_set (str): DRC rule set to use. Default is "sg13g2_minimal". Available options:
            - sg13g2_minimal
            - sg13g2_maximal
    
    Returns:
        tuple: Metrics and artifacts from the DRC run.
    """
    logging.info(f"Running klayout IHP130({drc_rule_set}) on {top_name}")

    artifacts = {
        "klayout_report_db": f"{result_dir}/drc_klayout_{drc_rule_set}_{top_name}.lyrdb",
        "klayout_log": f"drc_klayout_{drc_rule_set}_{top_name}.log",
        "drc_report_json": f"{result_dir}/drc_{drc_rule_set}_{top_name}.json",
    }

    lydrc_script = f"{R2G_PDK_DIR_IHP130}/ihp-sg13g2/libs.tech/klayout/tech/drc/{drc_rule_set}.lydrc"
    active_module = f"{top_name}"
    shell_cmd = [
        "klayout",
        "-b", # batch mode
        "-zz", # disable all GUI
        "-r",  lydrc_script,
        "-rd", f"log_file={artifacts['klayout_log']}",
        "-rd", f"in_gds={gds_file}",
        "-rd", f"cell={active_module}",
        "-rd", f"report_file={artifacts['klayout_report_db']}",
    ]

    logging.info(
        "(step.%s) \n subprocess cmd: %s \n",
        STEP_NAME,
        str(shell_cmd),
    )

    start_time = time.perf_counter()
    ret_code = subprocess.call(shell_cmd)
    end_time = time.perf_counter()
    logging.info("KLayout DRC elapsed time: %.2f seconds", end_time - start_time)

    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, shell_cmd)

    klayout_rdb = klayout.rdb.ReportDatabase("DRC")
    klayout_rdb.load(artifacts['klayout_report_db'])

    drc_categories = {}
    for category in klayout_rdb.each_category():
        drc_categories[category.name()] = category.num_items()

    # klayout_rdb.description: 'design rules: design_rule_name | layout cell: top_name'
    rule_actually_use = klayout_rdb.description.split('|')[0].strip().split(':', 1)[1].strip()
    assert rule_actually_use == drc_rule_set, f"DRC rule set mismatch: {rule_actually_use} != {drc_rule_set}"

    metrics = {
        "design_rule_set": drc_rule_set,
        "drc_violations": klayout_rdb.num_items(),
        "drc_categories": drc_categories,
    }

    with open(artifacts['drc_report_json'], 'w') as f:
        json.dump(metrics, f, indent=4)

    return metrics, artifacts

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    top_name = "tt_um_kianV_rv32ima_uLinux_SoC"
    gds_file = f"/home/user/demo/kianvconfigs/orfs/results/ihp-sg13g2/kianv/base/6_final.gds"
    result_dir = "./result"

    metrics, drc_res_files = run(top_name, gds_file, result_dir, tool="klayout")

    print("Metrics:", metrics)
    print("DRC Result Files:", drc_res_files)
