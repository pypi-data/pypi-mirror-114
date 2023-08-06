import logging
import sys
import time
from typing import Dict, Union

from dagster import check
from dagster.core.events.log import EventLogEntry
from dagster.core.host_representation import RepositoryLocationOrigin
from dagster.core.launcher.base import LaunchRunContext
from dagster.core.workspace.dynamic_workspace import DynamicWorkspace
from dagster.daemon.daemon import DagsterDaemon
from dagster.grpc.client import DagsterGrpcClient
from dagster.serdes import deserialize_json_to_dagster_namedtuple, serialize_dagster_namedtuple
from dagster.utils.error import serializable_error_info_from_exc_info
from dagster_cloud.api.dagster_cloud_api import (
    CheckForWorkspaceUpdatesSuccess,
    DagsterCloudApi,
    DagsterCloudApiErrorResponse,
    DagsterCloudApiGrpcResponse,
    DagsterCloudApiRequest,
    DagsterCloudApiSuccess,
)
from dagster_cloud.executor.step_handler_context import DagsterCloudStepHandlerContext
from dagster_cloud.instance import DagsterCloudAgentInstance
from dagster_cloud.workspace.origin import CodeDeploymentMetadata

from .queries import (
    GET_USER_CLOUD_REQUESTS_QUERY,
    SEND_USER_CLOUD_RESPONSE_MUTATION,
    WORKSPACE_ENTRIES_QUERY,
)


class DagsterCloudApiDaemon(DagsterDaemon):
    def __init__(self):
        self._initial_workspace_loaded = False
        super(DagsterCloudApiDaemon, self).__init__(interval_seconds=0.5)

    @classmethod
    def daemon_type(cls) -> str:
        return "DAGSTER_CLOUD_API"

    def _check_for_workspace_updates(
        self, instance: DagsterCloudAgentInstance, workspace: DynamicWorkspace
    ):
        workspace.cleanup()  # Clear any existing origins

        # Get list of workspace entries from DB
        result = instance.graphql_client.execute(WORKSPACE_ENTRIES_QUERY)
        entries = result["data"]["workspace"]["workspaceEntries"]

        # Create mapping of
        # - location name => deployment metadata
        deployment_map: Dict[str, CodeDeploymentMetadata] = {}
        force_update_locations = set()
        for entry in entries:
            location_name = entry["locationName"]
            deployment_metadata = check.inst(
                deserialize_json_to_dagster_namedtuple(entry["serializedDeploymentMetadata"]),
                CodeDeploymentMetadata,
            )
            deployment_map[location_name] = deployment_metadata
            if entry["hasOutdatedData"]:
                force_update_locations.add(location_name)

        workspace.grpc_server_registry.update_grpc_metadata(deployment_map, force_update_locations)

    def _get_grpc_client(
        self, workspace: DynamicWorkspace, repository_location_origin: RepositoryLocationOrigin
    ) -> DagsterGrpcClient:
        endpoint = workspace.grpc_server_registry.get_grpc_endpoint(repository_location_origin)
        return endpoint.create_client()

    def _handle_api_request(
        self,
        request: DagsterCloudApiRequest,
        instance: DagsterCloudAgentInstance,
        workspace: DynamicWorkspace,
    ) -> Union[
        CheckForWorkspaceUpdatesSuccess,
        DagsterCloudApiSuccess,
        DagsterCloudApiGrpcResponse,
    ]:
        api_name = request.request_api
        if api_name == DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES:
            self._check_for_workspace_updates(instance, workspace)
            return CheckForWorkspaceUpdatesSuccess()
        elif api_name == DagsterCloudApi.GET_EXTERNAL_EXECUTION_PLAN:
            external_pipeline_origin = request.request_args.pipeline_origin
            client = self._get_grpc_client(
                workspace,
                external_pipeline_origin.external_repository_origin.repository_location_origin,
            )
            serialized_snapshot_or_error = client.execution_plan_snapshot(
                execution_plan_snapshot_args=request.request_args
            )
            return DagsterCloudApiGrpcResponse(serialized_snapshot_or_error)

        elif api_name == DagsterCloudApi.GET_SUBSET_EXTERNAL_PIPELINE_RESULT:
            external_pipeline_origin = request.request_args.pipeline_origin
            client = self._get_grpc_client(
                workspace,
                external_pipeline_origin.external_repository_origin.repository_location_origin,
            )

            serialized_subset_result_or_error = client.external_pipeline_subset(
                pipeline_subset_snapshot_args=request.request_args
            )

            return DagsterCloudApiGrpcResponse(serialized_subset_result_or_error)
        elif api_name == DagsterCloudApi.GET_EXTERNAL_PARTITION_CONFIG:
            external_repository_origin = request.request_args.repository_origin
            client = self._get_grpc_client(
                workspace, external_repository_origin.repository_location_origin
            )
            serialized_partition_config_or_error = client.external_partition_config(
                partition_args=request.request_args,
            )
            return DagsterCloudApiGrpcResponse(serialized_partition_config_or_error)
        elif api_name == DagsterCloudApi.GET_EXTERNAL_PARTITION_TAGS:
            external_repository_origin = request.request_args.repository_origin
            client = self._get_grpc_client(
                workspace, external_repository_origin.repository_location_origin
            )
            serialized_partition_tags_or_error = client.external_partition_tags(
                partition_args=request.request_args,
            )
            return DagsterCloudApiGrpcResponse(serialized_partition_tags_or_error)
        elif api_name == DagsterCloudApi.GET_EXTERNAL_PARTITION_NAMES:
            external_repository_origin = request.request_args.repository_origin
            client = self._get_grpc_client(
                workspace, external_repository_origin.repository_location_origin
            )
            serialized_partition_names_or_error = client.external_partition_names(
                partition_names_args=request.request_args,
            )
            return DagsterCloudApiGrpcResponse(serialized_partition_names_or_error)
        elif api_name == DagsterCloudApi.GET_EXTERNAL_PARTITION_SET_EXECUTION_PARAM_DATA:
            external_repository_origin = request.request_args.repository_origin
            client = self._get_grpc_client(
                workspace, external_repository_origin.repository_location_origin
            )
            serialized_partition_execution_params_or_error = (
                client.external_partition_set_execution_params(
                    partition_set_execution_param_args=request.request_args
                )
            )
            return DagsterCloudApiGrpcResponse(serialized_partition_execution_params_or_error)
        elif api_name == DagsterCloudApi.GET_EXTERNAL_SCHEDULE_EXECUTION_DATA:
            external_repository_origin = request.request_args.repository_origin
            client = self._get_grpc_client(
                workspace, external_repository_origin.repository_location_origin
            )

            args = request.request_args._replace(instance_ref=instance.get_ref())

            serialized_schedule_data_or_error = client.external_schedule_execution(
                external_schedule_execution_args=args,
            )

            return DagsterCloudApiGrpcResponse(serialized_schedule_data_or_error)

        elif api_name == DagsterCloudApi.GET_EXTERNAL_SENSOR_EXECUTION_DATA:
            external_repository_origin = request.request_args.repository_origin
            client = self._get_grpc_client(
                workspace, external_repository_origin.repository_location_origin
            )

            args = request.request_args._replace(instance_ref=instance.get_ref())

            serialized_sensor_data_or_error = client.external_sensor_execution(
                sensor_execution_args=args,
            )

            return DagsterCloudApiGrpcResponse(serialized_sensor_data_or_error)
        elif api_name == DagsterCloudApi.LAUNCH_RUN:
            run = request.request_args.pipeline_run
            instance.report_engine_event(
                f"Received request from {instance.dagster_cloud_url} to launch all steps for pipeline {run.pipeline_name}",
                run,
                cls=self.__class__,
            )

            launcher = workspace.grpc_server_registry.run_launcher()
            launcher.launch_run(LaunchRunContext(pipeline_run=run, workspace=workspace))
            return DagsterCloudApiSuccess()
        elif api_name == DagsterCloudApi.TERMINATE_RUN:
            run = request.request_args.pipeline_run
            instance.report_engine_event(
                f"Received request from {instance.dagster_cloud_url} to terminate run",
                run,
                cls=self.__class__,
            )

            launcher = workspace.grpc_server_registry.run_launcher()
            launcher.terminate(run.run_id)
            return DagsterCloudApiSuccess()
        elif api_name == DagsterCloudApi.LAUNCH_STEP:
            context = DagsterCloudStepHandlerContext.deserialize(
                instance, request.request_args.persisted_step_handler_context
            )
            args = context.execute_step_args
            assert len(args.step_keys_to_execute) == 1
            step_key = args.step_keys_to_execute[0]

            instance.report_engine_event(
                f"Received request from {instance.dagster_cloud_url} to launch steps: {', '.join(args.step_keys_to_execute)}",
                context.pipeline_run,
                cls=self.__class__,
            )

            step_handler = workspace.grpc_server_registry.step_handler()
            events = step_handler.launch_step(context)
            for event in events:
                event_record = EventLogEntry(
                    message=event.message,
                    user_message=event.message,
                    level=logging.INFO,
                    pipeline_name=context.pipeline_run.pipeline_name,
                    run_id=context.pipeline_run.run_id,
                    error_info=None,
                    timestamp=time.time(),
                    step_key=step_key,
                    dagster_event=event,
                )
                instance.handle_new_event(event_record)

            return DagsterCloudApiSuccess()

        elif api_name == DagsterCloudApi.TERMINATE_STEP:
            context = DagsterCloudStepHandlerContext.deserialize(
                instance, request.request_args.persisted_step_handler_context
            )

            step_handler = workspace.grpc_server_registry.step_handler()
            events = step_handler.terminate_step(context)
            for event in events:
                instance.handle_new_event(event)

            return DagsterCloudApiSuccess()

        elif api_name == DagsterCloudApi.CHECK_STEP_HEALTH:
            context = DagsterCloudStepHandlerContext.deserialize(
                instance, request.request_args.persisted_step_handler_context
            )

            step_handler = workspace.grpc_server_registry.step_handler()
            events = step_handler.check_step_health(context)
            for event in events:
                instance.handle_new_event(event)

            return DagsterCloudApiSuccess()

        else:
            check.assert_never(api_name)
            raise Exception(
                "Unexpected dagster cloud api call {api_name}".format(api_name=api_name)
            )

    def run_iteration(self, instance: DagsterCloudAgentInstance, workspace: DynamicWorkspace):
        if not self._initial_workspace_loaded:
            self._check_for_workspace_updates(instance, workspace)
            self._initial_workspace_loaded = True

        result = instance.graphql_client.execute(GET_USER_CLOUD_REQUESTS_QUERY)

        requests = [
            deserialize_json_to_dagster_namedtuple(request["requestBody"])
            for request in result["data"]["userCloudAgent"]["popUserCloudAgentRequests"]
        ]

        for request in requests:
            self._logger.info(
                "Responding to API request {request_id}: {request_name} with args: {request_args}".format(
                    request_id=request.request_id,
                    request_name=request.request_api,
                    request_args=str(request.request_args) if request.request_args else "None",
                )
            )

            api_result: Union[
                CheckForWorkspaceUpdatesSuccess,
                DagsterCloudApiSuccess,
                DagsterCloudApiGrpcResponse,
                DagsterCloudApiErrorResponse,
                None,
            ] = None
            try:
                api_result = self._handle_api_request(request, instance, workspace)
            except Exception:  # pylint: disable=broad-except
                error_info = serializable_error_info_from_exc_info(sys.exc_info())
                api_result = DagsterCloudApiErrorResponse(error_infos=[error_info])
                self._logger.error(
                    "Error serving API request {request_id}: {request_name}:\n{error_info}".format(
                        request_id=request.request_id,
                        request_name=request.request_api,
                        error_info=str(error_info),
                    )
                )
                yield error_info

            response = serialize_dagster_namedtuple(api_result)

            # Check for errors
            instance.graphql_client.execute(
                SEND_USER_CLOUD_RESPONSE_MUTATION,
                {
                    "requestId": request.request_id,
                    "requestApi": request.request_api.value,
                    "response": response,
                },
            )

        yield
