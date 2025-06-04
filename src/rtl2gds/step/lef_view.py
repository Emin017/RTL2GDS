import logging
import os
import subprocess

from rtl2gds.global_configs import R2G_PDK_DIR_IHP130, R2G_TOOL_DIR, StepName


def save_abstract_lef(input_def: str, lef_file: str):
    """
    Generates an abstract LEF file using Magic.
    """

    artifacts = {
        "abstract_lef_file": lef_file,
    }

    # Prepare environment variables that the Tcl script will use
    pdk_stdcell_base = f"{R2G_PDK_DIR_IHP130}/ihp-sg13g2/libs.ref/sg13g2_stdcell"
    step_env = {
        "MAGIC_SCRIPTS_DIR": f"{R2G_TOOL_DIR}/magic",
        "TECH_LEF": f"{pdk_stdcell_base}/lef/sg13g2_tech.lef",
        "CELL_GDS": f"{pdk_stdcell_base}/gds/sg13g2_stdcell.gds",
    }

    # Prepare the command-line arguments for Magic and the Tcl script
    shell_cmd = [
        "magic",
        "-noconsole",
        "-dnull",
        "-rcfile",
        f"{R2G_PDK_DIR_IHP130}/ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc",
        f"{R2G_TOOL_DIR}/magic/lef.tcl",
        input_def,
        artifacts["abstract_lef_file"],
    ]

    full_env = os.environ.copy()
    full_env.update(step_env)

    logging.info(
        "(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
        StepName.ABSTRACT_LEF,
        str(shell_cmd),
        str(step_env),
    )

    try:
        e = subprocess.run(
            shell_cmd,
            check=True,
            text=True,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            env=full_env,
        )
        if e.returncode != 0:
            raise subprocess.CalledProcessError(e, shell_cmd)
        print("Magic stdout:", e.stdout)
        print("Magic stderr:", e.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' failed with signal or non-zero exit code {e.returncode}.")
        print("Magic stdout:", e.stdout)
        print("Magic stderr:", e.stderr)

    metrics = {}

    return metrics, artifacts


if __name__ == "__main__":
    r2g_base = "/opt/rtl2gds"

    save_abstract_lef(
        input_def=f"{r2g_base}/design_zoo/gcd/gcd_results/gcd_filler.def",
        lef_file=f"{r2g_base}/design_zoo/gcd/gcd_results/gcd.lef",
    )
