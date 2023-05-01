"""Process_instance."""
from __future__ import annotations

import sys
import typing
from dataclasses import dataclass
from typing import Any
from typing import cast

if sys.version_info < (3, 11):
    from typing_extensions import TypedDict, NotRequired
else:
    from typing import TypedDict, NotRequired
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from spiffworkflow_backend.models.db import db
from spiffworkflow_backend.models.db import SpiffworkflowBaseDBModel
from spiffworkflow_backend.models.json_data import JsonDataModel  # noqa: F401
from spiffworkflow_backend.models.process_instance import ProcessInstanceModel
from spiffworkflow_backend.models.user import UserModel
from spiffworkflow_backend.services.process_instance_processor import (
    ProcessInstanceProcessor,
)


class FilterValue(TypedDict):
    field_name: str
    field_value: str | int | bool
    operator: NotRequired[str]


class ReportMetadataColumn(TypedDict):
    Header: str
    accessor: str
    filterable: NotRequired[bool]


class ReportMetadata(TypedDict):
    columns: list[ReportMetadataColumn]
    filter_by: list[FilterValue]
    order_by: list[str]


class Report(TypedDict):
    id: int
    identifier: str
    name: str
    report_metadata: ReportMetadata


class ProcessInstanceReportAlreadyExistsError(Exception):
    """ProcessInstanceReportAlreadyExistsError."""


class ProcessInstanceReportResult(TypedDict):
    """ProcessInstanceReportResult."""

    report_metadata: ReportMetadata
    results: list[dict]


# https://stackoverflow.com/a/56842689/6090676
class Reversor:
    """Reversor."""

    def __init__(self, obj: Any):
        """__init__."""
        self.obj = obj

    def __eq__(self, other: Any) -> Any:
        """__eq__."""
        return other.obj == self.obj

    def __lt__(self, other: Any) -> Any:
        """__lt__."""
        return other.obj < self.obj


@dataclass
class ProcessInstanceReportModel(SpiffworkflowBaseDBModel):
    """ProcessInstanceReportModel."""

    __tablename__ = "process_instance_report"
    __table_args__ = (
        db.UniqueConstraint(
            "created_by_id",
            "identifier",
            name="process_instance_report_unique",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    identifier: str = db.Column(db.String(50), nullable=False, index=True)
    report_metadata: ReportMetadata = db.Column(db.JSON)
    created_by_id = db.Column(ForeignKey(UserModel.id), nullable=False, index=True)  # type: ignore
    created_by = relationship("UserModel")
    created_at_in_seconds = db.Column(db.Integer)
    updated_at_in_seconds = db.Column(db.Integer)

    json_data_hash: str = db.Column(db.String(255), nullable=False, index=True)

    def get_report_metadata(self) -> ReportMetadata:
        rdata_dict = JsonDataModel.find_data_dict_by_hash(self.json_data_hash)
        rdata = typing.cast(ReportMetadata, rdata_dict)
        return rdata

    @classmethod
    def default_order_by(cls) -> list[str]:
        """Default_order_by."""
        return ["-start_in_seconds", "-id"]

    @classmethod
    def create_report(
        cls,
        identifier: str,
        user: UserModel,
        report_metadata: ReportMetadata,
    ) -> ProcessInstanceReportModel:
        process_instance_report = ProcessInstanceReportModel.query.filter_by(
            identifier=identifier,
            created_by_id=user.id,
        ).first()

        if process_instance_report is not None:
            raise ProcessInstanceReportAlreadyExistsError(
                f"Process instance report with identifier already exists: {identifier}"
            )

        report_metadata_dict = typing.cast(typing.Dict[str, Any], report_metadata)
        json_data_hash = JsonDataModel.create_and_insert_json_data_from_dict(report_metadata_dict)

        process_instance_report = cls(
            identifier=identifier,
            created_by_id=user.id,
            report_metadata=report_metadata,
            json_data_hash=json_data_hash,
        )
        db.session.add(process_instance_report)
        db.session.commit()

        return process_instance_report  # type: ignore

    def with_substitutions(self, field_value: Any, substitution_variables: dict) -> Any:
        if substitution_variables is not None:
            for key, value in substitution_variables.items():
                if isinstance(value, str) or isinstance(value, int):
                    field_value = str(field_value).replace("{{" + key + "}}", str(value))
        return field_value

    # modeled after https://github.com/suyash248/sqlalchemy-json-querybuilder
    # just supports "equals" operator for now.
    # perhaps we will use the database instead of filtering in memory in the future and then we might use this lib directly.
    def passes_filter(self, process_instance_dict: dict, substitution_variables: dict) -> bool:
        """Passes_filter."""
        if "filter_by" in self.report_metadata:
            for filter_by in self.report_metadata["filter_by"]:
                field_name = filter_by["field_name"]
                operator = filter_by["operator"]
                field_value = self.with_substitutions(filter_by["field_value"], substitution_variables)
                if operator == "equals":
                    if str(process_instance_dict.get(field_name)) != str(field_value):
                        return False

        return True

    def order_things(self, process_instance_dicts: list) -> list:
        """Order_things."""
        order_by = self.report_metadata["order_by"]

        def order_by_function_for_lambda(
            process_instance_dict: dict,
        ) -> list[Reversor | str | None]:
            """Order_by_function_for_lambda."""
            comparison_values: list[Reversor | str | None] = []
            for order_by_item in order_by:
                if order_by_item.startswith("-"):
                    # remove leading - from order_by_item
                    order_by_item = order_by_item[1:]
                    sort_value = process_instance_dict.get(order_by_item)
                    comparison_values.append(Reversor(sort_value))
                else:
                    sort_value = cast(Optional[str], process_instance_dict.get(order_by_item))
                    comparison_values.append(sort_value)
            return comparison_values

        return sorted(process_instance_dicts, key=order_by_function_for_lambda)

    def generate_report(
        self,
        process_instances: list[ProcessInstanceModel],
        substitution_variables: dict | None,
    ) -> ProcessInstanceReportResult:
        """Generate_report."""
        if substitution_variables is None:
            substitution_variables = {}

        def to_serialized(process_instance: ProcessInstanceModel) -> dict:
            """To_serialized."""
            processor = ProcessInstanceProcessor(process_instance)
            process_instance.data = processor.get_current_data()
            return process_instance.serialized_flat

        process_instance_dicts = map(to_serialized, process_instances)
        results = []
        for process_instance_dict in process_instance_dicts:
            if self.passes_filter(process_instance_dict, substitution_variables):
                results.append(process_instance_dict)

        if "order_by" in self.report_metadata:
            results = self.order_things(results)

        if "columns" in self.report_metadata:
            column_keys_to_keep = [c["accessor"] for c in self.report_metadata["columns"]]

            pruned_results = []
            for result in results:
                dict_you_want = {
                    your_key: result[your_key] for your_key in column_keys_to_keep if result.get(your_key)
                }
                pruned_results.append(dict_you_want)
            results = pruned_results

        return ProcessInstanceReportResult(report_metadata=self.report_metadata, results=results)
