from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import datetime
from typing import Generator, Optional

from sqlmodel import Field, SQLModel, create_engine, Session, select


DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "flows.db"))
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})


class FlowORM(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def upsert_flow(flow_id: str, name: str, json_text: str) -> FlowORM:
    with get_session() as session:
        existing: Optional[FlowORM] = session.get(FlowORM, flow_id)
        if existing is None:
            flow = FlowORM(id=flow_id, name=name, json=json_text)
            session.add(flow)
        else:
            existing.name = name
            existing.json = json_text
            existing.updated_at = datetime.utcnow()
            flow = existing
        session.commit()
        session.refresh(flow)
        return flow


def get_flow(flow_id: str) -> Optional[FlowORM]:
    with get_session() as session:
        return session.get(FlowORM, flow_id)


def list_flows() -> list[FlowORM]:
    with get_session() as session:
        results = session.exec(select(FlowORM)).all()
        return list(results)