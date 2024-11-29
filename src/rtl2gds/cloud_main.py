#!/usr/bin/env python3
"""module main"""
import logging
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import requests
import yaml

from rtl2gds.chip import Chip
from rtl2gds.flow import cloud_flow
from rtl2gds.global_configs import StepName


@dataclass
class NotifyTaskBody:
    """
    NotifyTaskBody example:
    {
        "taskID": "${uuid}",
        "taskName": "",
        "serverTimestamp": 1724814202505,
        "files": [
            "gds-${uuid}-1.json",
            "gds-${uuid}-2.json",
            "gds-${uuid}-3.json",
            "gds-${uuid}-4.json"
        ],
        "userID":  112,
        "projectID": 3
    }
    """

    files: List[str]
    server_timestamp: int
    status: str
    task_id: str
    task_type: str
    task_name: Optional[str] = None


def _get_timestamp() -> str:
    return str(datetime.now())


def _notify_task(layout_files: list):
    # notify_server = "192.168.0.10:8083"
    notify_server = "localhost:8083"
    notify_path = "/apis/v1/notify/task"
    notify_url = notify_server + notify_path
    json_body = NotifyTaskBody(
        files=layout_files,
        server_timestamp=_get_timestamp(),
        status="success",
        task_id=uuid.uuid4(),
        task_type="@TODO",
    )
    response = requests.post(
        url=notify_url,
        json=json_body,
        timeout=5.0,
    )
    print(
        f"POST request response: success?({response.status_code == 200}) {response.text}"
    )


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

    layout_json_files = cloud_flow.run(chip_design, expect_step=step)

    chip_design.dump_config()

    # Notify task results
    _notify_task(layout_json_files)


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
