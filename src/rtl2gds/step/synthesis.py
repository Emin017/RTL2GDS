"""
Synthesis step implementation using yosys
"""

import logging
import math
import os
import subprocess
import tempfile

from ..global_configs import ENV_TOOLS_PATH, StepName
from .configs import SHELL_CMD
from .synth_util import SynthStatParser

MAX_CELL_AREA = 1_000_000


def save_module_preview(verilog_file, output_svg=None, module_name=None, flatten=False,
                          aig=False, skin_file=None):
    """
    Export a Verilog to an SVG diagram preview using **Yosys** and **netlistsvg**.

    Args:
        verilog_file (str): Path to the input Verilog file
        output_svg (str, optional): Path to the output SVG file. Defaults to input filename or module_name with .svg extension.
        module_name (str, optional): Name of the top module. If None, Yosys will auto-detect.
        flatten (bool, optional): If True, flatten the design to basic logic gates. Defaults to False.
        aig (bool, optional): If True, convert to AND-inverter graph representation. Defaults to False.
        skin_file (str, optional): Path to a custom skin file for netlistsvg. Defaults to None.

    Returns:
        str: Path to the generated SVG file

    Raises:
        FileNotFoundError: If the input Verilog file doesn't exist
        subprocess.CalledProcessError: If Yosys or netlistsvg commands fail
    """
    # Check if input file exists
    if not os.path.isfile(verilog_file):
        raise FileNotFoundError(f"Input Verilog file not found: {verilog_file}")

    # Set default output SVG filename if not provided
    if output_svg is None:
        base_name = os.path.splitext(verilog_file)[0] if module_name is None else module_name
        output_svg = f"{base_name}.svg"

    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_json:
        json_file = temp_json.name

    try:
        # Construct Yosys command
        yosys_cmd = ["yosys", "-p"]

        # Build the prep command
        prep_cmd = "prep"
        if module_name:
            prep_cmd += f" -top {module_name}"
        if flatten:
            prep_cmd += " -flatten"

        # Complete Yosys command
        if aig:
            yosys_cmd_str = f"{prep_cmd}; aigmap; write_json {json_file}"
        else:
            yosys_cmd_str = f"{prep_cmd}; write_json {json_file}"

        yosys_cmd.append(yosys_cmd_str)
        yosys_cmd.append(verilog_file)

        # Run Yosys
        # https://github.com/nturley/netlistsvg/blob/master/README.md#generating-input_json_file-with-yosys
        # yosys -p "prep -top my_top_module; write_json output.json" input.v
        # yosys -p "prep -top my_top_module -flatten; write_json output.json" input.v
        # yosys -p "prep -top my_top_module; aigmap; write_json output.json" input.v
        print(f"Running Yosys: {' '.join(yosys_cmd)}")
        subprocess.run(yosys_cmd, check=True, env=ENV_TOOLS_PATH)

        # Construct netlistsvg command
        netlistsvg_cmd = ["netlistsvg", json_file, "-o", output_svg]
        if skin_file:
            netlistsvg_cmd.extend(["--skin", skin_file])

        # Run netlistsvg
        # netlistsvg input_json_file [-o output_svg_file] [--skin skin_file]
        print(f"Running netlistsvg: {' '.join(netlistsvg_cmd)}")
        subprocess.run(netlistsvg_cmd, check=True)

        print(f"SVG diagram generated successfully: {output_svg}")
        return output_svg

    finally:
        # Clean up temporary JSON file
        if os.path.exists(json_file):
            os.remove(json_file)

def convert_sv2v(input_sv, output_v, top=None, write=None, incdir=None, define=None):
    """
    Converts a SystemVerilog file to Verilog using sv2v.

    Args:
        input_sv (str): Path to the input SystemVerilog file.
        output_v (str): Path to the output Verilog file.
        incdir (list, optional): List of include directories. Defaults to None.
        define (list, optional): List of define. Defaults to None.

    Returns:
        bool: True if conversion was successful, False otherwise.
    """

    # import shutil; shutil.which("sv2v")
    sv2v_executable = 'sv2v'
    if not sv2v_executable:
        print("Error: sv2v is not installed or not in PATH.")
        return False

    cmd = [sv2v_executable, input_sv, "-w", output_v]  # Basic sv2v command
    if incdir:
        for incdir in incdir:
            cmd.extend(["-I", incdir])
    if define:
        for define in define:
            cmd.extend(["-D", f"{define}"])  # Assumes define is in NAME=VALUE format
    if top:
        cmd.extend(["--top", top])
    if write:
        cmd.extend(["-w", write])

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, env=ENV_TOOLS_PATH)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running sv2v: {e}")
        print(f"sv2v stdout: {e.stdout}")  # Capture and print stdout/stderr for debugging
        print(f"sv2v stderr: {e.stderr}")
        return False

def parse_synth_stat(report_path: str):
    """Extract top module area and name from yosys report and simplify cell names"""
    found_top_summary = False
    stats = {
        "total_cells": 0,
        "cell_area": 0.0,
        "sequential_ratio": 0.0,
        "cell_types": {}
    }
    cell_prefix = "sky130_fd_sc_hs__"
    cell_prefix_match_pattern = f"     {cell_prefix}"

    with open(report_path, "r", encoding="utf-8") as file:
        for line in file:
            if found_top_summary:
                if "Chip area for top module" in line:
                    # Extract the area from the line
                    parts = line.split(":")
                    # We don't need the module name, just the area
                    stats["cell_area"] = float(parts[1].strip())
                elif "Number of cells" in line:
                    stats["total_cells"] = int(line.split(":")[1].strip())
                elif line.startswith(cell_prefix_match_pattern):
                    cell_type, count = line.strip().rsplit(" ", 1)
                    cell_name = cell_type.strip().replace(cell_prefix, "")
                    cell_count = int(count)
                    stats["cell_types"][cell_name] = cell_count

            if "=== design hierarchy ===" in line:
                found_top_summary = True

    if not found_top_summary:
        raise RuntimeError("Missing top module in synthesis report")

    return stats

def _convert_sv_to_v(rtl_file: str | list[str], result_dir: str, top_name: str) -> str | list[str]:
    """Convert SystemVerilog files to Verilog format if necessary.

    Args:
        rtl_file: Path(s) to the input RTL file(s)
        result_dir: Directory to store converted Verilog files
        top_name: Name of the top-level module

    Returns:
        Path(s) to the converted Verilog file(s)

    Raises:
        RuntimeError: If SystemVerilog conversion fails
    """
    if isinstance(rtl_file, str) and rtl_file.endswith('.sv'):
        if not os.path.exists(rtl_file):
            raise FileNotFoundError(f"RTL file {rtl_file} not found")
        converted_v_file = f"{result_dir}/{os.path.basename(rtl_file).replace('.sv', '.v')}"
        if not convert_sv2v(rtl_file, converted_v_file, top=top_name):
            raise RuntimeError(f"Failed to convert SystemVerilog file {rtl_file} to Verilog")
        return converted_v_file
    elif isinstance(rtl_file, list) and any(file.endswith('.sv') for file in rtl_file):
        converted_v_files = []
        for file in rtl_file:
            if not os.path.exists(file):
                raise FileNotFoundError(f"RTL file {file} not found")
            if file.endswith('.sv'):
                converted_v_file = f"{result_dir}/{os.path.basename(file).replace('.sv', '.v')}"
                if not convert_sv2v(file, converted_v_file, top=top_name):
                    raise RuntimeError(f"Failed to convert SystemVerilog file {file} to Verilog")
                converted_v_files.append(converted_v_file)
            else:
                converted_v_files.append(file)
        return converted_v_files
    return rtl_file

def _setup_step_env(top_name, rtl_file, netlist_file, sdc_file, synth_stat_txt, synth_check_txt,
                   clk_port_name, clk_freq_mhz):
    """Setup environment variables for Yosys synthesis.

    Args:
        top_name (str): Name of the top-level module
        rtl_file (str): Path to the input RTL file
        netlist_file (str): Path to the output netlist file
        sdc_file (str): Path to the SDC constraint file
        yosys_report_dir (str): Directory for Yosys reports
        clk_port_name (str): Name of the clock port
        clk_freq_mhz (str): Clock frequency in MHz

    Returns:
        dict: Environment variables for synthesis
    """
    step_env = {
        "TOP_NAME": str(top_name),
        "RTL_FILE": str(rtl_file),
        "NETLIST_FILE": str(netlist_file),
        "SDC_FILE": str(sdc_file),
        "SYNTH_STAT_TXT": str(synth_stat_txt),
        "SYNTH_CHECK_TXT": str(synth_check_txt),
        "CLK_PORT_NAME": str(clk_port_name),
        "CLK_FREQ_MHZ": str(clk_freq_mhz),
    }

    step_env.update(ENV_TOOLS_PATH)
    return step_env

def _calculate_areas(cell_area, core_util, die_bbox=None, core_bbox=None):
    """Calculate die and core areas based on synthesis statistics.

    Args:
        stats (dict): Synthesis statistics from Yosys
        core_util (float): Core utilization percentage
        die_bbox (str, optional): Die area coordinates. Defaults to None
        core_bbox (str, optional): Core area coordinates. Defaults to None

    Returns:
        tuple: (die_bbox, core_bbox, core_util)
    """
    if not (die_bbox and core_bbox):
        core_length = math.sqrt(cell_area / core_util)
        io_margin = 10
        die_bbox = f"0 0 {core_length+io_margin*2} {core_length+io_margin*2}"
        core_bbox = (
            f"{io_margin} {io_margin} {core_length+io_margin} {core_length+io_margin}"
        )

    elif not core_util:
        core = core_bbox.split(" ")
        core_len_x = float(core[2]) - float(core[0])
        core_len_y = float(core[3]) - float(core[1])
        core_area = core_len_x * core_len_y
        core_util = cell_area / core_area
        assert 0 < core_util < 1, "Core utilization out of range"

    return die_bbox, core_bbox, core_util

def run(
    top_name: str,
    rtl_file: str | list[str],
    netlist_file: str,
    sdc_file: str,
    result_dir: str,
    clk_port_name: str,
    clk_freq_mhz: str,
    die_bbox: str | None = None,
    core_bbox: str | None = None,
    core_util: float | None = None,
):
    """Run synthesis step using Yosys.

    Args:
        top_name (str): Name of the top-level module
        rtl_file (str | list[str]): Path(s) to the input RTL file(s)
        netlist_file (str): Path to the output netlist file
        sdc_file (str): Path to the SDC constraint file
        result_dir (str): Directory to store synthesis results
        clk_port_name (str): Name of the clock port
        clk_freq_mhz (str): Clock frequency in MHz
        die_bbox (str, optional): Die area coordinates. Defaults to None
        core_bbox (str, optional): Core area coordinates. Defaults to None
        core_util (float, optional): Core utilization percentage. Defaults to None

    Returns:
        dict: Dictionary containing synthesis results including:
            - DIE_AREA: Die area coordinates
            - CORE_AREA: Core area coordinates
            - CORE_UTIL: Core utilization percentage
            - TOTAL_CELLS: Total number of cells
            - CELL_AREA: Total cell area
            - CELL_TYPES: Dictionary of cell types and their counts

    Raises:
        subprocess.CalledProcessError: If synthesis fails
        AssertionError: If required parameters are missing or invalid
        RuntimeError: If SystemVerilog conversion fails
    """
    # Convert SystemVerilog files if necessary and also check RTL file existence
    rtl_file = _convert_sv_to_v(rtl_file, result_dir, top_name)

    # flatten rtl_file if it is a list (pass ENV var to yosys.tcl)
    if isinstance(rtl_file, list):
        rtl_file = " \n ".join(rtl_file)

    step_cmd = SHELL_CMD[StepName.SYNTHESIS]

    # Setup Yosys report directory
    yosys_report_dir = f"{result_dir}/report"
    os.makedirs(yosys_report_dir, exist_ok=True)

    artifacts = {
        "synth_stat_txt": f"{yosys_report_dir}/synth_stat.txt",
        "synth_check_txt": f"{yosys_report_dir}/synth_check.txt",
        "netlist": netlist_file,
    }

    # Setup environment variables
    step_env = _setup_step_env(top_name, rtl_file, netlist_file, sdc_file,
        artifacts['synth_stat_txt'], artifacts['synth_check_txt'], clk_port_name, clk_freq_mhz)

    # Run synthesis
    logging.info("(step.%s) \n subprocess cmd: %s \n subprocess env: %s",
                StepName.SYNTHESIS, str(step_cmd), step_env)

    try:
        ret_code = subprocess.call(step_cmd, env=step_env)
        if ret_code != 0:
            raise subprocess.CalledProcessError(ret_code, step_cmd)
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            output=f"Synthesis step failed with return code {e.returncode}"
        ) from e

    # collect results
    synth_stat = artifacts["synth_stat_txt"]
    assert os.path.exists(synth_stat), "Synthesis statistic file not found"
    assert os.path.exists(netlist_file), "Netlist file not found"

    stats = parse_synth_stat(synth_stat)
    cell_area = stats["cell_area"]
    assert 0 < cell_area < MAX_CELL_AREA, "Cell area exceeds processing limit"

    # Calculate areas
    die_bbox, core_bbox, core_util = _calculate_areas(cell_area, core_util, die_bbox, core_bbox)

    metrics = {
        "die_bbox": die_bbox,
        "core_bbox": core_bbox,
        "core_util": core_util,
        "total_cells": stats["total_cells"],
        "cell_area": cell_area,
        # "cell_types": stats["cell_types"]
    }

    return metrics, artifacts

if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
        level=logging.INFO,
    )

    logging.info("Testing synthesis...")

    # Setup test design
    TEST_DESIGN_TOP = "aes_cipher_top"
    test_rtl = [
        "/home/wsl/rtl2gds/design_zoo/aes/aes_cipher_top.v",
        "/home/wsl/rtl2gds/design_zoo/aes/aes_inv_cipher_top.v",
        "/home/wsl/rtl2gds/design_zoo/aes/aes_inv_sbox.v",
        "/home/wsl/rtl2gds/design_zoo/aes/aes_key_expand_128.v",
        "/home/wsl/rtl2gds/design_zoo/aes/aes_rcon.v",
        "/home/wsl/rtl2gds/design_zoo/aes/aes_sbox.v",
        "/home/wsl/rtl2gds/design_zoo/aes/timescale.v",
    ]
    RESULT_DIR = "./results"
    OUTPUT_NETLIST = "./results/aes_netlist.v"

    import shutil

    shutil.rmtree(RESULT_DIR)

    from ..chip.design_constrain import DesignConstrain
    from ..chip.design_path import DesignPath
    from ..global_configs import DEFAULT_SDC_FILE

    path_setting = DesignPath(
        rtl_file=test_rtl,
        result_dir=RESULT_DIR,
        netlist_file=OUTPUT_NETLIST,
        sdc_file=DEFAULT_SDC_FILE,
    )
    constrain = DesignConstrain(clk_port_name="clk", clk_freq_mhz="100", core_util=0.5)

    env = run(
        top_name=TEST_DESIGN_TOP, design_path=path_setting, design_constrain=constrain
    )

    logging.info("Synthesis completed successfully")
    logging.info("Generated netlist: %s", env["NETLIST_FILE"])
    logging.info("Die area: %s", env["DIE_AREA"])
    logging.info("Core area: %s", env["CORE_AREA"])
    logging.info("env: %s", env)
