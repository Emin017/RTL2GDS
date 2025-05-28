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

import logging
import os
from pathlib import Path

from kubernetes import client, config

# load ServiceAccount token
config.load_incluster_config()
logging.info("Loaded in-cluster Kubernetes config.")


def start_rtl2gds_job(
    job_name: str,
    job_workspace_path: Path,
    job_config_path: Path,
    job_rtl_path: Path,
    flow_step: str = "rtl2gds_all",
    pvc_name: str = os.getenv("PVC_NAME", "eda-server-pvc"),
    job_image: str = "rtl2gds:latest",
    namespace: str = os.getenv("K8S_NAMESPACE", "eda"),
    front_service_name: str = os.getenv("FRONT_SERVICE_HOST", "mock-front-svc"),
    front_port: int = os.getenv("FRONT_SERVICE_PORT", 8083),
    job_ttl_seconds: int = 3600
) -> str:
    """
    Starts a Kubernetes Job to run the RTL2GDS process.

    Args:
        host_workspace: Path within the API pod's PVC mount for the workspace.
        host_config: Path within the API pod's PVC mount for the config file.
        host_rtl: Path within the API pod's PVC mount for the RTL file.
        flow_step: The specific RTL2GDS step to run.
        pvc_name: The name of the PersistentVolumeClaim used for data sharing.
        job_image: The container image to use for the Job.
        namespace: The Kubernetes namespace where the Job will be created.
        front_service_name: The name of the mock_front Kubernetes service.
        front_port: The port of the front Kubernetes service.
        job_ttl_seconds: Time in seconds after which a finished Job should be cleaned up.

    Returns:
        A status message indicating whether the Job was created successfully.
    """
    logging.info(f"Attempting to start Kubernetes Job for step '{flow_step}' in namespace '{namespace}'")

    api_instance = client.BatchV1Api()

    # --- Define Job Structure ---
    mount_path_in_job_pod = "/projectData" # Job Pod 内挂载 PVC 的路径
    guest_r2g_module = "/opt/rtl2gds/src"
    guest_r2g_entry = f"{guest_r2g_module}/rtl2gds/cloud_main.py"

    # Job Pod 内的路径应与 API Pod 传入的路径匹配（因为共享同一个 PVC）
    # 但需要确保它们指向 PVC 挂载点内部
    # 假设 API Pod 和 Job Pod 都将 PVC 挂载到 /projectData
    # host_workspace 已经是 /projectData/<projectID>
    # host_config    已经是 /projectData/<projectID>/config.yaml
    # host_rtl       已经是 /projectData/<projectID>/top.v
    job_workspace_path = str(job_workspace_path)
    job_config_path = str(job_config_path)
    job_rtl_path = str(job_rtl_path)

    # 构造 front 的内部 URL
    front_url = f"http://{front_service_name}.{namespace}.svc.cluster.local:{front_port}/apis/v1/notify/task"

    # 1. Define Volume Mount (for the container)
    volume_mount = client.V1VolumeMount(
        name="eda-server-data",  # Must match the volume name below
        mount_path=mount_path_in_job_pod # PVC 在 Job Pod 内的挂载点
    )

    # 2. Define Volume (referencing the PVC)
    volume = client.V1Volume(
        name="eda-server-data", # Must match volume_mount's name
        persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name=pvc_name)
    )

    # 3. Define Environment Variables for the Job container
    env_vars = [
        client.V1EnvVar(name="FRONT_URL", value=front_url),
        # client.V1EnvVar(name="LOG_LEVEL", value=os.getenv("JOB_LOG_LEVEL", "INFO"))
    ]

    # 4. Define the Container spec
    container = client.V1Container(
        name="rtl2gds-worker",
        image=job_image,
        command=["/usr/bin/env", "python3", guest_r2g_entry],
        args=[
            job_rtl_path,      # Arg 1: RTL file path inside Job Pod
            job_config_path,   # Arg 2: Config file path inside Job Pod
            job_workspace_path,# Arg 3: Workspace path inside Job Pod
            flow_step            # Arg 4: Flow step name
        ],
        env=env_vars,
        volume_mounts=[volume_mount],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "2", "memory": "4Gi"},
            limits={"cpu": "4", "memory": "8Gi"}
        )
    )

    # 5. Define the Pod Template Spec
    pod_template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "rtl2gds-worker", "job-name": job_name}),
        spec=client.V1PodSpec(
            restart_policy="Never",
            containers=[container],
            volumes=[volume],
            # service_account_name= # 如果 Job Pod 需要特殊权限，指定 ServiceAccount
        )
    )

    # 6. Define the Job Spec
    job_spec = client.V1JobSpec(
        template=pod_template,
        backoff_limit=1,  # 重试次数 (0 表示不重试)
        ttl_seconds_after_finished=job_ttl_seconds # 自动清理已完成的 Job
        # active_deadline_seconds= # 可选：设置 Job 的最长运行时间
    )

    # 7. Create the Job Object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name, namespace=namespace),
        spec=job_spec
    )

    # 8. Create the Job in Kubernetes
    try:
        api_response = api_instance.create_namespaced_job(body=job, namespace=namespace)
        logging.info(f"Successfully created Kubernetes Job: {api_response.metadata.name}")
        return f"Kubernetes Job '{api_response.metadata.name}' created successfully for step '{flow_step}'."
    except client.ApiException as e:
        logging.error(f"Exception when calling BatchV1Api->create_namespaced_job: {e}\nBody: {job}")
        error_details = e.body
        return f"Failed to create Kubernetes Job for step '{flow_step}'. Error: {error_details}"
    except Exception as e:
        logging.exception(f"An unexpected error occurred when creating Kubernetes job: {e}")
        error_details = e.body
        return f"Failed to create Kubernetes Job for step '{flow_step}'. Unexpected error: {error_details}."
