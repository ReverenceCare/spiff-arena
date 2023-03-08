from __future__ import annotations

from sqlalchemy import ForeignKey

from spiffworkflow_backend.models.db import db
from spiffworkflow_backend.models.db import SpiffworkflowBaseDBModel


# properties_json attributes:
#   "last_task", # guid generated by spiff
#   "root", # guid generated by spiff
#   "success", # boolean
#   "bpmn_messages", # if top-level process
#   "correlations", # if top-level process
class BpmnProcessModel(SpiffworkflowBaseDBModel):
    __tablename__ = "bpmn_process"
    id: int = db.Column(db.Integer, primary_key=True)
    guid: str | None = db.Column(db.String(36), nullable=True, unique=True, index=True)

    parent_process_id: int | None = db.Column(
        ForeignKey("bpmn_process.id"), nullable=True
    )

    properties_json: dict = db.Column(db.JSON, nullable=False)
    json_data_hash: str = db.Column(db.String(255), nullable=False, index=True)

    # subprocess or top_level_process
    # process_type: str = db.Column(db.String(30), nullable=False)

    # FIXME: find out how to set this but it'd be cool
    start_in_seconds: float = db.Column(db.DECIMAL(17, 6))
    end_in_seconds: float | None = db.Column(db.DECIMAL(17, 6))