import logging
import os
from pathlib import Path
from typing import Optional

import uvicorn
import yaml
import uuid
from call_service import start_rtl2gds_job
from fastapi import FastAPI
from pydantic import BaseModel

from rtl2gds.global_configs import RTL2GDS_FLOW_STEP, StepName

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()


class StdinEDA(BaseModel):
    code: str
    ownerID: str
    projectID: str
    userID: str  # not in use
    filePath: Optional[str] = None


class ResponseData(BaseModel):
    code: str


class ResponseModel(BaseModel):
    code: int
    message: str
    data: Optional[ResponseData] = None


@app.post("/apis/v1/ieda/stdin", response_model=ResponseModel)
async def call_ieda(stdin: StdinEDA) -> ResponseModel:
    """
    Handles requests to trigger RTL2GDS flow steps via Kubernetes Jobs.
    """
    logging.info(f"Received request: {stdin}")

    try:
        command_parts = stdin.code.split()
        if len(command_parts) < 2:
             logging.warning("Invalid command format in request code.")
             return ResponseModel(code=400, message="Bad Request: Command must be in format 'run step_name'", data=ResponseData(code="INVALID_COMMAND_FORMAT"))

        step_name = command_parts[1]
        if step_name not in RTL2GDS_FLOW_STEP:
            logging.warning(f"Invalid step name received: {step_name}")
            return ResponseModel(code=404, message=f"Not Found: Step '{step_name}' is not a valid flow step", data=ResponseData(code="INVALID_STEP_NAME"))

        mount_point = Path("/projectData")
        if not mount_point.is_dir():
             logging.error(f"PVC mount point {mount_point} not found or is not a directory inside the pod.")
             return ResponseModel(code=503, message="Service Unavailable: Storage system not accessible", data=ResponseData(code="STORAGE_UNAVAILABLE"))

        eda_workspace = mount_point / stdin.projectID   # /projectData/<projectID>
        cloud_config = eda_workspace / "config.yaml"    # /projectData/<projectID>/config.yaml
        rtl_file = eda_workspace / "top.v"              # /projectData/<projectID>/top.v

        if not eda_workspace.is_dir():
             logging.error(f"Eda workspace {eda_workspace} not found or is not a directory.")
             return ResponseModel(code=404, message="Not Found: EDA workspace does not exist", data=ResponseData(code="WORKSPACE_NOT_FOUND"))
        if not cloud_config.is_file():
             logging.warning(f"Config file not found at: {cloud_config}")
             return ResponseModel(code=404, message="Not Found: Configuration file is missing", data=ResponseData(code="CONFIG_NOT_FOUND"))
        if not rtl_file.is_file():
             logging.warning(f"RTL file not found at: {rtl_file}")
             return ResponseModel(code=404, message="Not Found: RTL file is missing", data=ResponseData(code="RTL_NOT_FOUND"))

        validation_response = is_valid_config(cloud_config, step_name)
        if validation_response.code != 0:
            logging.warning(f"Configuration validation failed: {validation_response.message}")
            return validation_response

        logging.info("Configuration validated successfully. Starting Kubernetes Job...")
        response_message = start_rtl2gds_job(
            job_name=f"rtl2gds-{stdin.projectID}-{step_name}-{uuid.uuid4().hex[:6]}",
            job_workspace_path=eda_workspace,
            job_config_path=cloud_config,
            job_rtl_path=rtl_file,
            flow_step=step_name,
            pvc_name=os.getenv("PVC_NAME", "eda-data-pvc"),
            namespace=os.getenv("NAMESPACE", "eda"),
        )

        logging.info(f"Job creation response: {response_message}")
        # 根据 start_rtl2gds_service 的返回消息判断成功或失败
        if "Failed" in response_message:
             return ResponseModel(code=500, message="Internal Server Error: Failed to create backend job", data=ResponseData(code="JOB_CREATION_FAILED"))
        else:
             return ResponseModel(code=0, message="Accepted: Job submitted successfully", data=ResponseData(code="JOB_SUBMITTED"))

    except Exception as e:
        logging.exception(f"An unexpected error occurred in call_ieda: {e}")
        return ResponseModel(code=500, message=f"Internal Server Error: Unexpected server error: {e}", data=ResponseData(code="INTERNAL_ERROR"))

def get_expected_step(finished_step: str) -> Optional[str]:
    try:
        index = RTL2GDS_FLOW_STEP.index(finished_step)
        if index == len(RTL2GDS_FLOW_STEP) - 1:
            return None
        return RTL2GDS_FLOW_STEP[index + 1]
    except ValueError:
        return None

def is_valid_config(config_path: Path, step_name: str) -> ResponseModel:
    """Validates the configuration file."""
    logging.info(f"Validating config file: {config_path} for step: {step_name}")
    if not config_path.is_file():
        return ResponseModel(code=404, message="Not Found: Config file does not exist", data=ResponseData(code="CONFIG_FILE_NOT_FOUND"))

    required_keys = ["TOP_NAME", "CLK_PORT_NAME"]

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if config is None:
                 logging.warning(f"Config file {config_path} is empty.")
                 return ResponseModel(code=400, message="Bad Request: Config file is empty", data=ResponseData(code="EMPTY_CONFIG"))

        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            msg = f"Missing required keys in config: {', '.join(missing_keys)}"
            logging.warning(msg)
            return ResponseModel(code=400, message="Bad Request: Invalid configuration", data=ResponseData(code="MISSING_CONFIG_KEYS"))

        if "FINISHED_STEP" in config:
            finished_step = config["FINISHED_STEP"]
            expected_next_step = get_expected_step(finished_step)
            logging.info(f"Config indicates finished step: {finished_step}. Expected next step: {expected_next_step}")
            if step_name != StepName.RTL2GDS_ALL and expected_next_step != step_name:
                msg = f"Invalid step sequence. Expected {expected_next_step} after {finished_step}, got {step_name}"
                logging.warning(msg)
                return ResponseModel(code=409, message=f"Conflict: {msg}", data=ResponseData(code="INVALID_STEP_SEQUENCE"))
        elif step_name != StepName.RTL2GDS_ALL and step_name != StepName.SYNTHESIS:
            msg = f"Must start with {StepName.RTL2GDS_ALL} or {StepName.SYNTHESIS}"
            logging.warning(msg)
            return ResponseModel(code=400, message=f"Bad Request: Invalid starting step. {msg}", data=ResponseData(code="INVALID_INITIAL_STEP"))

    except yaml.YAMLError as e:
         logging.error(f"Failed to parse YAML config {config_path}: {e}")
         return ResponseModel(code=400, message="Bad Request: Invalid YAML format", data=ResponseData(code="INVALID_YAML"))
    except Exception as e:
        logging.exception(f"Unexpected error during config validation for {config_path}: {e}")
        return ResponseModel(code=500, message="Internal Server Error: Config validation failed", data=ResponseData(code="VALIDATION_ERROR"))

    logging.info("Config validation successful.")
    return ResponseModel(code=0, message="OK: Config validation successful")


@app.get("/hello")
def get_hello():
    return {"Hello": "RTL2GDS K8s API YES!"}


if __name__ == "__main__":
    eda_service_host = os.getenv("EDA_SERVICE_HOST", "10.233.50.10")
    eda_service_port = 9444
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    print(f"Starting RTL2GDS API server on {eda_service_host}:{eda_service_port}")
    uvicorn.run(
        app="cloud:app",
        host=eda_service_host,
        port=eda_service_port,
        log_level=log_level,
        reload=False,
    )
