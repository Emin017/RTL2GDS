"""
WORKSPACE=f"{mount_point}/{stdin.project_id}"
PYTHONPATH="/opt/rtl2gds/src"
docker run --rm -it 
-v ${WORKSPACE}:${WORKSPACE} 
-v ${WORKSPACE}/config.yaml:${WORKSPACE}/config.yaml 
-v ${WORKSPACE}/top.v:${WORKSPACE}/top.v 
--net eda-subnet 
--env PYTHONPATH=${PYTHONPATH}
rtl2gds:latest 
/usr/bin/env python3 ${PYTHONPATH}/rtl2gds/cloud_main.py ${WORKSPACE}/top.v ${WORKSPACE}/config.yaml ${WORKSPACE}
"""

import pathlib

import docker

client = docker.from_env()


def start_rtl2gds_service(
    host_workspace: pathlib.Path,
    host_config: pathlib.Path,
    host_rtl: pathlib.Path,
    flow_step: str = "rtl2gds_all",
) -> str:
    """
    start a rtl2gds container
    running the container in detach mode
    @TODO: a callback function for a costum request?
    return status message
    """

    guest_r2g_module = "/opt/rtl2gds/src"
    guest_r2g_entry = f"{guest_r2g_module}/rtl2gds/cloud_main.py"
    guest_workspace = host_workspace  # must match
    guest_config = f"{guest_workspace}/config.yaml"
    guest_rtl_file = f"{guest_workspace}/top.v"
    container = client.containers.run(
        "rtl2gds:latest",
        volumes={
            host_workspace: {"bind": guest_workspace, "mode": "rw"},
            host_config: {"bind": guest_config, "mode": "rw"},
            host_rtl: {"bind": guest_rtl_file, "mode": "ro"},
        },
        network="eda-subnet",
        auto_remove=True,
        detach=True,
        environment={"PYTHONPATH": guest_r2g_module},
        command=[
            "/usr/bin/env",
            "python3",
            guest_r2g_entry,
            guest_rtl_file,
            guest_config,
            guest_workspace,
            flow_step,
        ],
    )

    return f"Container({container.id}) started, running {flow_step} backend..."
