from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import threading
import uuid
from typing import Any, AsyncGenerator, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

try:
    from .db import DB_PATH, FlowORM, get_flow, init_db, list_flows, upsert_flow
    from .models import CreateFlowRequest, Flow, UpdateFlowRequest
except Exception:  # pragma: no cover
    from db import DB_PATH, FlowORM, get_flow, init_db, list_flows, upsert_flow  # type: ignore
    from models import CreateFlowRequest, Flow, UpdateFlowRequest  # type: ignore

app = FastAPI(title="Lindy PocketFlow Builder")

# CORS (dev-friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize DB at startup
@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/flows")
async def get_flows() -> list[Flow]:
    flows: list[Flow] = []
    for orm in list_flows():
        data = json.loads(orm.json)
        flows.append(Flow.model_validate(data))
    return flows


@app.post("/flows")
async def create_flow(payload: CreateFlowRequest) -> Flow:
    flow_id = str(uuid.uuid4())
    flow = Flow(
        id=flow_id,
        name=payload.name,
        nodes=payload.nodes,
        edges=payload.edges,
        pocketflow_code="",
    )
    upsert_flow(flow_id, flow.name, flow.model_dump_json())
    return flow


@app.get("/flows/{flow_id}")
async def get_flow_by_id(flow_id: str) -> Flow:
    orm: Optional[FlowORM] = get_flow(flow_id)
    if orm is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    return Flow.model_validate_json(orm.json)


@app.put("/flows/{flow_id}")
async def update_flow(flow_id: str, payload: UpdateFlowRequest) -> Flow:
    orm: Optional[FlowORM] = get_flow(flow_id)
    if orm is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    data = json.loads(orm.json)
    if payload.name is not None:
        data["name"] = payload.name
    if payload.nodes is not None:
        data["nodes"] = [n.model_dump() for n in payload.nodes]
    if payload.edges is not None:
        data["edges"] = [e.model_dump() for e in payload.edges]
    flow = Flow.model_validate(data)
    upsert_flow(flow_id, flow.name, flow.model_dump_json())
    return flow


# Simple in-memory job registry
class JobState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    job_id: str
    flow_id: str
    queue: asyncio.Queue[str]
    done: asyncio.Event


_jobs: dict[str, JobState] = {}


@app.post("/flows/{flow_id}/run")
async def run_flow(flow_id: str) -> Dict[str, str]:
    orm: Optional[FlowORM] = get_flow(flow_id)
    if orm is None:
        raise HTTPException(status_code=404, detail="Flow not found")

    job_id = str(uuid.uuid4())
    queue: asyncio.Queue[str] = asyncio.Queue()
    done_event = asyncio.Event()
    state = JobState(job_id=job_id, flow_id=flow_id, queue=queue, done=done_event)
    _jobs[job_id] = state

    # Launch runner as subprocess
    backend_dir = os.path.dirname(__file__)
    python_exe = sys.executable

    process = await asyncio.create_subprocess_exec(
        python_exe,
        os.path.join(backend_dir, "runner.py"),
        flow_id,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=backend_dir,
        env={**os.environ, "DB_PATH": DB_PATH},
    )

    async def read_stdout() -> None:
        assert process.stdout is not None
        try:
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                await queue.put(line.decode(errors="ignore").rstrip("\n"))
        finally:
            await process.wait()
            done_event.set()
            await queue.put("__EOF__")

    asyncio.create_task(read_stdout())

    return {"job_id": job_id}


@app.get("/flows/{flow_id}/logs/{job_id}")
async def stream_logs(flow_id: str, job_id: str) -> StreamingResponse:
    state = _jobs.get(job_id)
    if state is None or state.flow_id != flow_id:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator() -> AsyncGenerator[bytes, None]:
        while True:
            line = await state.queue.get()
            if line == "__EOF__":
                yield f"event: end\ndata: done\n\n".encode()
                break
            # SSE format
            payload = line.replace("\n", " ")
            yield f"data: {payload}\n\n".encode()

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/templates")
async def list_templates() -> Dict[str, Any]:
    # Placeholder hard-coded templates for now
    return {
        "templates": [
            {"id": "resume-rag", "name": "Resume RAG"},
            {"id": "code-gen", "name": "Code Generator"},
            {"id": "map-reduce", "name": "Map-Reduce"},
        ]
    }