import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import requests

from .. import step
from ..chip import Chip
from ..global_configs import StepName
from . import rtl2gd_flow
from .step_runner import StepRunner


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


def run(chip: Chip, expect_step: str = StepName.RTL2GDS_ALL):

    dump_json = False
    if expect_step == StepName.RTL2GDS_ALL:
        rtl2gd_flow.run(chip)
        dump_json = True
    else:
        runner = StepRunner(chip)

        if expect_step == StepName.SYNTHESIS:
            runner.run_synthesis()
        elif expect_step == StepName.FLOORPLAN:
            runner.run_floorplan()
            runner.run_dump_layout_gds(step_name=expect_step, take_snapshot=True)
            # dump_json = True
        else:
            runner.run_pr_step(expect_step)
            if expect_step in [
                StepName.PLACE,
                StepName.CTS,
                StepName.LEGALIZE,
                StepName.ROUTE,
                StepName.FILLER,
            ]:
                runner.run_dump_layout_gds(step_name=expect_step, take_snapshot=True)
            # dump_json = True

    # Dump and return json files
    if dump_json:
        json_files = step.dump_layout_json.run(
            input_def=chip.path_setting.def_file,
            result_dir=chip.path_setting.result_dir,
            layout_json_file=f"{chip.path_setting.result_dir}/{chip.design_top}_{chip.finished_step}.json",
        )
    else:
        json_files = "?"

    # Notify task results
    _notify_task(json_files)
