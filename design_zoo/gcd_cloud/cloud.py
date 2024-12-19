import os
from dataclasses import dataclass
from typing import Optional

import uvicorn
import yaml
from call_service import start_rtl2gds_service
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@dataclass
class StdinEDA(BaseModel):
    code: str
    ownerID: str
    projectID: str
    userID: str  # not in use
    filePath: Optional[str] = None


@dataclass
class ResponseData:
    code: str


@dataclass
class Response:
    code: int
    message: str
    data: Optional[ResponseData] = None


@app.post("/apis/v1/ieda/stdin")
async def call_ieda(stdin: StdinEDA) -> Response:
    """
    request(StdinEDA) body:
    {
        "code": "user input commands",
        "userID": "user id",
        "projectID":"project id",
        "ownerID":"owner id"
    }
    """
    print(stdin)

    step_name = stdin.code.split(" ")[1]
    if step_name not in RTL2GDS_FLOW_STEP:
        return Response(code=0, message="bad", data=ResponseData("Invalid step name"))

    mount_point = "/data/eda-project-cos"
    eda_workspace = f"{mount_point}/{stdin.projectID}"
    cloud_config = f"{eda_workspace}/gcd.yaml"
    rtl_file = f"{eda_workspace}/gcd.v"

    response = is_valid_config(cloud_config, step_name)
    if response.code == 0:
        return response

    response_data = start_rtl2gds_service(
        host_workspace=eda_workspace,
        host_config=cloud_config,
        host_rtl=rtl_file,
        flow_step=step_name,
    )

    print(f"Response: {response_data}")
    return Response(code=1, message="ok", data=ResponseData(response_data))


@dataclass
class StepName:
    """RTL2GDS flow step names"""

    RTL2GDS_ALL = "rtl2gds_all"
    SYNTHESIS = "synthesis"
    FLOORPLAN = "floorplan"
    FIXFANOUT = "fixfanout"
    PLACE = "place"
    CTS = "cts"
    DRV_OPT = "drv_opt"
    HOLD_OPT = "hold_opt"
    LEGALIZE = "legalize"
    ROUTE = "route"
    FILLER = "filler"


RTL2GDS_FLOW_STEP = [
    StepName.RTL2GDS_ALL,
    StepName.SYNTHESIS,
    StepName.FLOORPLAN,
    StepName.FIXFANOUT,
    StepName.PLACE,
    StepName.CTS,
    StepName.DRV_OPT,
    StepName.HOLD_OPT,
    StepName.LEGALIZE,
    StepName.ROUTE,
    StepName.FILLER,
]


def get_expected_step(finished_step: str) -> Optional[str]:
    """Get the expected step for the rtl2gds flow"""
    if finished_step == RTL2GDS_FLOW_STEP[-1]:
        return None
    return RTL2GDS_FLOW_STEP[RTL2GDS_FLOW_STEP.index(finished_step) + 1]


def is_valid_config(cloud_config: str, step_name: str) -> Response:
    # Check if config file exists and is valid
    if not os.path.exists(cloud_config):
        return Response(
            code=0,
            message="bad",
            data=ResponseData(f"Config file {cloud_config} does not exist"),
        )

    required_keys = ["DESIGN_TOP", "CLK_PORT_NAME", "CLK_FREQ_MHZ", "CORE_UTIL"]

    try:
        with open(cloud_config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Check required keys exist
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            return Response(
                code=0,
                message="bad",
                data=ResponseData(
                    f"Missing required keys in config: {', '.join(missing_keys)}"
                ),
            )

        if "FINISHED_STEP" in config:
            except_step = get_expected_step(config["FINISHED_STEP"])
            if except_step != step_name:
                return Response(
                    code=0,
                    message="bad",
                    data=ResponseData(
                        f"Invalid step name, expected {except_step}, got {step_name}"
                    ),
                )

    except Exception as e:
        return Response(
            code=0, message="bad", data=f"Failed to validate config: {str(e)}"
        )

    return Response(code=1, message="ok")


@app.get("/hello")
def get_hello():
    return {"Hello": "RTL2GDS YES!"}


# docker run -it --rm --net eda-subnet \
#  --ip 192.168.0.12 -p 9444:9444 --name r2gcloud \
#  -v ${mount_point}:${mount_point} \
#  -v /var/run/docker.sock:/var/run/docker.sock \
#  -v $(which docker):/usr/bin/docker \
#  r2gcloud:latest python3 /opt/r2gcloud/cloud.py
if __name__ == "__main__":
    # $uvicorn main:app --reload --port 9444 --log-level info (default)
    SERVER_IP = "192.168.0.12"
    # SERVER_IP = "localhost"
    SERVER_PORT = 9444
    uvicorn.run(
        app="cloud:app",
        host=SERVER_IP,
        port=SERVER_PORT,
        log_level="info",
        reload=False,
    )
