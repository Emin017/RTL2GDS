from dataclasses import dataclass
from typing import List, Optional

import uvicorn
from fastapi import FastAPI

# from . import api_config


@dataclass
class Request:
    files: List[str]
    server_timestamp: int
    status: str
    task_id: str
    task_type: str
    task_name: Optional[str] = None

    def __str__(self) -> str:
        return f"Request(task_id={self.task_id}\ntime={self.server_timestamp}\ntask_type={self.task_type}\nstatus={self.status}\nfiles={self.files})"


app = FastAPI()


@app.get("/hello")
def get_hello():
    return {"Hello": "Mock front YES!"}


# test front-end server
@app.post("/apis/v1/notify/task")
async def mock_front(r2g_done: Request):
    print(str(r2g_done))


# docker run -it --net eda-subnet --ip 192.168.0.10 -p 8083:8083 --rm \
#  --name mock_front r2gcloud:latest python3 /opt/r2gcloud/mock_front.py
if __name__ == "__main__":
    # $uvicorn main:app --reload --port 8666 --log-level info (default)
    front_ip = "192.168.0.10"
    front_port = 8083
    uvicorn.run(
        app="mock_front:app",
        host=front_ip,
        port=front_port,
        log_level="info",
        reload=False,
    )
