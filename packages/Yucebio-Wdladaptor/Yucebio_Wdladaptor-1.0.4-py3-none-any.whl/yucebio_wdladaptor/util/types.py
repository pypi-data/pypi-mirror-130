from typing import Any, TypedDict


class CromwellBackendType(TypedDict):
    name: str
    owner: str
    alias: str
    host: str
    platform: str
    global_path: str
    simg_path: str

class RestfulResponseType(TypedDict):
    code: int
    message: str
    data: Any


class WorkflowType(TypedDict):
    _id: str
    prefix: str
    cromwell_id: str
    workflow_name: str
    backend: CromwellBackendType

    status: str
    submission: str
    start: str
    end: str

    owner: str
    sample_ids: str
    running_tasks: list[str]

    calls: dict