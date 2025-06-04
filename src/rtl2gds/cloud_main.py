#!/usr/bin/env python3
"""module main"""
import logging
import os
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

import requests
import yaml

from rtl2gds.chip import Chip
from rtl2gds.flow import single_step
from rtl2gds.global_configs import StepName


@dataclass
class NotifyTaskBody:
    files: list[str]
    server_timestamp: int
    status: str
    task_id: str
    task_type: str


class NotifyStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    SUCCESS = "success"
    FAIL = "fail"
    QUEUEING = "queueing"
    STOPPING = "stopping"
    STOPPED = "stopped"


def _notify_task(
    result_files: dict,
    status: NotifyStatus = NotifyStatus.SUCCESS,
    task_id: str = None,
    task_type: str = "RTL2GDS_STEP",
):
    notify_url = os.getenv("FRONT_URL")
    if not notify_url:
        logging.error("FRONT_URL environment variable not set. Cannot notify.")
        # notify_url = "http://mock-front-svc.default.svc.cluster.local:8083/apis/v1/notify/task"
        return  # 决定不发送通知

    logging.info(f"Sending notification to: {notify_url}")

    if task_id is None:
        task_id = str(uuid.uuid4())
    json_body = NotifyTaskBody(
        files=result_files,
        server_timestamp=int(datetime.now().timestamp()),
        status=status,
        task_id=task_id,
        task_type=task_type,
    )
    logging.info(f"Notification body: {json_body}")
    try:
        response = requests.post(
            url=notify_url,
            headers={"Content-Type": "application/json"},
            json=asdict(json_body),
            timeout=10.0,
        )
        response.raise_for_status()
        logging.info(
            f"POST request response: status_code={response.status_code}, text={response.text}"
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send notification to {notify_url}: {e}")


def main():
    """
    rtl2gds cloud init
    Command: python3 /<rtl2gds-module>/cloud_main.py <rtl_file_path> <config_yaml_path> <workspace_path> [step_name]
    """
    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d]: %(message)s",
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
    logging.info(f"Starting cloud_main.py with args: {sys.argv}")

    if len(sys.argv) < 4:
        logging.error(
            "Insufficient arguments. Usage: python cloud_main.py <rtl_path> <config_yaml> <workspace_path> [step_name]"
        )
        sys.exit(1)

    rtl_path = Path(sys.argv[1])
    config_yaml = Path(sys.argv[2])
    workspace_path = Path(sys.argv[3])

    if not rtl_path.exists():
        logging.error(f"RTL file not found: {rtl_path}")
        sys.exit(1)
    if not config_yaml.exists():
        logging.error(f"Config file not found: {config_yaml}")
        sys.exit(1)
    if not workspace_path.is_dir():
        logging.error(f"Workspace path is not a directory or does not exist: {workspace_path}")
        sys.exit(1)

    step = StepName.RTL2GDS_ALL
    if len(sys.argv) == 5:
        step = sys.argv[4]
    logging.info(f"Target step: {step}")

    try:
        logging.info(f"Generating complete config in: {config_yaml}")
        generate_complete_config(config_yaml, rtl_path, workspace_path)

        logging.info("Initializing Chip design...")
        chip_design = Chip(config_yaml=config_yaml)

        logging.info(f"Running flow step: {step}")
        result_files = single_step.run(chip_design, expect_step=step)
        logging.info(f"Step {step} completed. Result files: {result_files}")

        logging.info("Dumping final config YAML...")
        chip_design.dump_config_yaml()

        logging.info("Notifying results...")
        _notify_task(result_files)
        logging.info("Notification process finished.")

    except Exception as e:
        logging.exception(f"An error occurred during the RTL2GDS process: {e}")
        _notify_task(
            [],
            status=NotifyStatus.FAIL,
            task_id=str(uuid.uuid4()),
            task_type="RTL2GDS_STEP",
        )
        sys.exit(1)

    logging.info("cloud_main.py finished successfully.")


def generate_complete_config(config_yaml: Path, rtl_path: Path, workspace_path: Path):
    """Loads, completes, and saves the configuration YAML."""
    logging.info(f"Loading config from {config_yaml}")
    with open(config_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        if config is None:
            config = {}
            logging.warning(f"Config file {config_yaml} was empty.")

    config["RTL_FILE"] = str(rtl_path.resolve())
    workspace_abs_path = str(workspace_path.resolve())

    required_keys = ["TOP_NAME", "CLK_PORT_NAME"]
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        error_msg = f"Missing required keys in config.yaml: {', '.join(missing_keys)}"
        logging.error(error_msg)
        raise ValueError(error_msg)

    top_name = config["TOP_NAME"]
    default_configs = {
        "RESULT_DIR": workspace_abs_path,
        "NETLIST_FILE": f"{workspace_abs_path}/{top_name}.v",
        "GDS_FILE": f"{workspace_abs_path}/{top_name}.gds",
        "CLK_FREQ_MHZ": 50,
        "CORE_UTIL": 0.5,
    }

    for key, value in default_configs.items():
        if key not in config:
            config[key] = value

    logging.info(f"Saving updated config to {config_yaml}")
    with open(config_yaml, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False)


if __name__ == "__main__":
    main()
