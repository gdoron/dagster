from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional


class DagsterGraphQLClientError(Exception):
    def __init__(self, *args, body=None):
        super().__init__(*args)
        self.body = body


class ReloadRepositoryLocationStatus(Enum):
    """This enum describes the status of a GraphQL mutation to reload a Dagster repository location

    Args:
        Enum (str): can be either `ReloadRepositoryLocationStatus.SUCCESS`
            or `ReloadRepositoryLocationStatus.FAILURE`.
    """

    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class ReloadRepositoryLocationInfo(NamedTuple):
    """This class gives information about the result of reloading
    a Dagster repository location with a GraphQL mutation.

    Args:
        status (ReloadRepositoryLocationStatus): The status of the reload repository location mutation
        failure_type: (Optional[str], optional): the failure type if `status == ReloadRepositoryLocationStatus.FAILURE`.
          Can be one of `ReloadNotSupported`, `RepositoryLocationNotFound`, or `RepositoryLocationLoadFailure`. Defaults to None.
        message (Optional[str], optional): the failure message/reason if
          `status == ReloadRepositoryLocationStatus.FAILURE`. Defaults to None.
    """

    status: ReloadRepositoryLocationStatus
    failure_type: Optional[str] = None
    message: Optional[str] = None


class PipelineInfo(NamedTuple):
    repository_location_name: str
    repository_name: str
    pipeline_name: str

    @staticmethod
    def from_node(node: Dict[str, Any]) -> List["PipelineInfo"]:
        repo_name = node["name"]
        repo_location_name = node["location"]["name"]
        return [
            PipelineInfo(
                repository_location_name=repo_location_name,
                repository_name=repo_name,
                pipeline_name=pipeline["name"],
            )
            for pipeline in node["pipelines"]
        ]


class InvalidOutputErrorInfo(NamedTuple):
    """This class gives information about an InvalidOutputError from submitting a pipeline for execution
    from GraphQL.

    Args:
        step_key (str): key of the step that failed
        invalid_output_name (str): the name of the invalid output from the given step
    """

    step_key: str
    invalid_output_name: str
