#!/usr/bin/env python3
"""module main"""
import logging
import sys
from pathlib import Path

import yaml

from rtl2gds.chip import Chip
from rtl2gds.flow import cloud_flow
from rtl2gds.global_configs import StepName

def main():
    """
    rtl2gds cloud init
    python3 /rtl2gds_module/cloud_main.py "/path/to/rtl_file" "/path/to/config.yaml" "/path/to/workspace" [step_name]
    """
    assert Path(sys.argv[1]).exists() and Path(sys.argv[2]).exists()

    rtl_path = sys.argv[1]
    config_yaml = sys.argv[2]
    workspace_path = sys.argv[3]

    step = StepName.RTL2GDS_ALL
    if len(sys.argv) == 5:
        step = sys.argv[4]

    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s", level="INFO"
    )

    generate_complete_config(config_yaml, rtl_path, workspace_path)
    chip_design = Chip(config_yaml)

    cloud_flow.run(chip_design, expect_step=step)

    chip_design.dump_config()


def generate_complete_config(config_yaml: str, rtl_path: str, workspace_path: str):
    with open(config_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["RTL_FILE"] = rtl_path
    required_keys = ["DESIGN_TOP", "CLK_PORT_NAME"]
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(f"Missing required keys in config: {', '.join(missing_keys)}")

    top_name = config["DESIGN_TOP"]
    default_configs = {
        "RESULT_DIR": f"{workspace_path}",
        "NETLIST_FILE": f"{workspace_path}/{top_name}.v",
        "GDS_FILE": f"{workspace_path}/{top_name}.gds",
        "CLK_PORT_NAME": config["CLK_PORT_NAME"],
        "CLK_FREQ_MHZ": 100,
        "CORE_UTIL": 0.6,
    }

    for key, value in default_configs.items():
        if key not in config:
            config[key] = value

    with open(config_yaml, "w", encoding="utf-8") as f:
        yaml.dump(config, f)

    # return config


if __name__ == "__main__":
    main()
