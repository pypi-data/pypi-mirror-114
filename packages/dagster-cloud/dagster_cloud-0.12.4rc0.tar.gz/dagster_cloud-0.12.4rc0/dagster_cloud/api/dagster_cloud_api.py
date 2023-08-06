from collections import namedtuple
from datetime import timedelta
from enum import Enum
from typing import Any, List, NamedTuple, Optional

import pendulum
from dagster import check
from dagster.core.code_pointer import CodePointer
from dagster.core.host_representation import ExternalRepositoryData, RepositoryLocationOrigin
from dagster.core.storage.pipeline_run import PipelineRun
from dagster.serdes import whitelist_for_serdes
from dagster.utils.error import SerializableErrorInfo
from dagster_cloud.executor.step_handler_context import PersistedDagsterCloudStepHandlerContext
from dagster_cloud.workspace.origin import CodeDeploymentMetadata

DEFAULT_EXPIRATION_MILLISECONDS = 10 * 60 * 1000


@whitelist_for_serdes
class DagsterCloudUploadRepositoryData(NamedTuple):
    """
    Serialized object uploaded by the Dagster Cloud agent with information pulled
    from a gRPC server about an individual repository - the data field is serialized since the
    agent may be running older code that doesn't know how to deserialize it, so it passes
    it serialized up to the host cloud, which is always up to date.
    """

    repository_name: str
    code_pointer: CodePointer
    serialized_repository_data: str


@whitelist_for_serdes
class DagsterCloudUploadLocationData(NamedTuple):
    """
    Serialized object uploaded by the Dagster Cloud agent with information pulled
    about a successfully loaded repository location, including information about
    each repository as well as shared metadata like the image to use when launching
    runs in this location.
    """

    upload_repository_datas: List[DagsterCloudUploadRepositoryData]
    container_image: Optional[str]
    executable_path: Optional[str]


@whitelist_for_serdes
class DagsterCloudUploadWorkspaceEntry(NamedTuple):
    """
    Serialized object uploaded by the Dagster Cloud agent with information about
    a repository location - either the serialized DagsterCloudUploadLocationData
    if the location loaded succesfully, or a SerializableErrorInfo describing the
    error if it was not.
    """

    location_name: str
    deployment_metadata: CodeDeploymentMetadata
    upload_location_data: Optional[DagsterCloudUploadLocationData]
    serialized_error_info: Optional[SerializableErrorInfo]


@whitelist_for_serdes
class DagsterCloudWorkspaceEntry(
    namedtuple(
        "_DagsterCloudWorkspaceEntry",
        "location_name deployment_metadata load_repositories_response serialized_error_info timestamp data_updated_timestamp",
    )
):
    """This class is deprecated and only exists for back-compat with pre-0.12.3 agents that
    fetched it over GraphQL and uploaded it to the server when writing repository location
    information. It can be removed once all agents using Dagster Cloud are at least
    at version 0.12.3."""

    def __new__(
        cls,
        location_name,
        deployment_metadata,
        load_repositories_response=None,
        serialized_error_info=None,
        timestamp=None,
        data_updated_timestamp=None,
    ):
        return super(DagsterCloudWorkspaceEntry, cls).__new__(
            cls,
            check.str_param(location_name, "location_name"),
            check.opt_inst_param(
                deployment_metadata, "deployment_metadata", CodeDeploymentMetadata
            ),
            check.opt_inst_param(
                load_repositories_response, "load_repositories_response", LoadRepositoriesResponse
            ),
            check.opt_inst_param(
                serialized_error_info, "serialized_error_info", SerializableErrorInfo
            ),
            check.opt_float_param(
                timestamp,
                "timestamp",
            ),
            check.opt_float_param(
                data_updated_timestamp,
                "data_updated_timestamp",
            ),
        )


@whitelist_for_serdes
class DagsterCloudApi(Enum):
    CHECK_FOR_WORKSPACE_UPDATES = "CHECK_FOR_WORKSPACE_UPDATES"
    LOAD_REPOSITORIES = "LOAD_REPOSITORIES"
    GET_EXTERNAL_EXECUTION_PLAN = "GET_EXTERNAL_EXECUTION_PLAN"
    GET_SUBSET_EXTERNAL_PIPELINE_RESULT = "GET_SUBSET_EXTERNAL_PIPELINE_RESULT"
    GET_EXTERNAL_PARTITION_CONFIG = "GET_EXTERNAL_PARTITION_CONFIG"
    GET_EXTERNAL_PARTITION_TAGS = "GET_EXTERNAL_PARTITION_TAGS"
    GET_EXTERNAL_PARTITION_NAMES = "GET_EXTERNAL_PARTITION_NAMES"
    GET_EXTERNAL_PARTITION_SET_EXECUTION_PARAM_DATA = (
        "GET_EXTERNAL_PARTITION_SET_EXECUTION_PARAM_DATA"
    )
    GET_EXTERNAL_SCHEDULE_EXECUTION_DATA = "GET_EXTERNAL_SCHEDULE_EXECUTION_DATA"
    GET_EXTERNAL_SENSOR_EXECUTION_DATA = "GET_EXTERNAL_SENSOR_EXECUTION_DATA"

    LAUNCH_RUN = "LAUNCH_RUN"
    TERMINATE_RUN = "TERMINATE_RUN"
    LAUNCH_STEP = "LAUNCH_STEP"
    CHECK_STEP_HEALTH = "CHECK_STEP_HEALTH"
    TERMINATE_STEP = "TERMINATE_STEP"


@whitelist_for_serdes
class DagsterCloudApiSuccess(namedtuple("_DagsterCloudApiSuccess", "")):
    pass


@whitelist_for_serdes
class CheckForWorkspaceUpdatesSuccess(namedtuple("_CheckForWorkspaceUpdatesSuccess", "")):
    pass


@whitelist_for_serdes
class LoadRepositoriesArgs(namedtuple("_LoadRepositoryArgs", "location_origin")):
    def __new__(cls, location_origin):
        return super(cls, LoadRepositoriesArgs).__new__(
            cls,
            check.inst_param(location_origin, "location_origin", RepositoryLocationOrigin),
        )


@whitelist_for_serdes
class DagsterCloudRepositoryData(
    namedtuple("_DagsterCloudRepositoryData", "repo_name code_pointer external_repository_data")
):
    def __new__(cls, repo_name, code_pointer, external_repository_data):
        return super(cls, DagsterCloudRepositoryData).__new__(
            cls,
            check.str_param(repo_name, "repo_name"),
            check.inst_param(code_pointer, "code_pointer", CodePointer),
            check.inst_param(
                external_repository_data,
                "external_repository_data",
                ExternalRepositoryData,
            ),
        )


@whitelist_for_serdes
class LoadRepositoriesResponse(
    namedtuple("_LoadRepositoriesResponse", "repository_datas container_image executable_path")
):
    def __new__(cls, repository_datas, container_image, executable_path):
        return super(cls, LoadRepositoriesResponse).__new__(
            cls,
            check.list_param(
                repository_datas,
                "repository_datas",
                of_type=DagsterCloudRepositoryData,
            ),
            check.opt_str_param(container_image, "container_image"),
            check.opt_str_param(executable_path, "executable_path"),
        )


@whitelist_for_serdes
class DagsterCloudApiErrorResponse(namedtuple("DagsterCloudApiErrorResponse", "error_infos")):
    def __new__(cls, error_infos):
        return super(cls, DagsterCloudApiErrorResponse).__new__(
            cls,
            check.list_param(error_infos, "error_infos", of_type=SerializableErrorInfo),
        )


@whitelist_for_serdes
class DagsterCloudApiGrpcResponse(
    namedtuple("DagsterCloudApiGrpcResponse", "serialized_response_or_error")
):
    # Class that DagsterCloudApi methods can use to pass along the result of
    # a gRPC call against the user code server. The field here is passed in
    # serialized as a string, because we can't guarantee that the agent code will
    # be up-to-date enough to know how to deserialize it (but the host cloud always
    # should, since it will always be up to date).
    def __new__(cls, serialized_response_or_error):
        return super(cls, DagsterCloudApiGrpcResponse).__new__(
            cls,
            check.str_param(serialized_response_or_error, "serialized_response_or_error"),
        )


@whitelist_for_serdes
class LaunchRunArgs(namedtuple("_LaunchRunArgs", "pipeline_run")):
    def __new__(cls, pipeline_run):
        return super(cls, LaunchRunArgs).__new__(
            cls,
            check.inst_param(pipeline_run, "pipeline_run", PipelineRun),
        )


@whitelist_for_serdes
class TerminateRunArgs(namedtuple("_TerminateRunArgs", "pipeline_run")):
    def __new__(cls, pipeline_run):
        return super(cls, TerminateRunArgs).__new__(
            cls,
            check.inst_param(pipeline_run, "pipeline_run", PipelineRun),
        )


@whitelist_for_serdes
class StepHandlerArgs(namedtuple("_StepHandlerArgs", "persisted_step_handler_context")):
    def __new__(cls, persisted_step_handler_context: PersistedDagsterCloudStepHandlerContext):
        return super(cls, StepHandlerArgs).__new__(
            cls,
            check.inst_param(
                persisted_step_handler_context,
                "persisted_step_handler_context",
                PersistedDagsterCloudStepHandlerContext,
            ),
        )


@whitelist_for_serdes
class DagsterCloudApiRequest(
    NamedTuple(
        "_DagsterCloudApiRequest",
        [
            ("request_id", str),
            ("request_api", DagsterCloudApi),
            ("request_args", Any),
            ("expire_at", float),
        ],
    )
):
    def __new__(
        cls,
        request_id: str,
        request_api: DagsterCloudApi,
        request_args: Any,
        expire_at: Optional[float] = None,
    ):
        return super(cls, DagsterCloudApiRequest).__new__(
            cls,
            check.str_param(request_id, "request_id"),
            check.inst_param(request_api, "request_api", DagsterCloudApi),
            request_args,
            check.opt_float_param(
                expire_at,
                "expire_at",
                default=(
                    pendulum.now("UTC") + timedelta(milliseconds=DEFAULT_EXPIRATION_MILLISECONDS)
                ).timestamp(),
            ),
        )

    @property
    def is_expired(self):
        return pendulum.now("UTC").timestamp() > self.expire_at
