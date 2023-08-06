import pytest
from dagster import graph, op, repository
from dagster.core.host_representation.origin import RegisteredRepositoryLocationOrigin
from dagster.core.workspace.dynamic_workspace import DynamicWorkspace
from dagster_cloud.api.dagster_cloud_api import DagsterCloudApi
from dagster_cloud.daemon.dagster_cloud_api_daemon import DagsterCloudApiDaemon
from dagster_cloud.workspace.origin import CodeDeploymentMetadata
from ursula.storage.host_cloud.cloud_storage.schema import (
    RepositoryLocationsDataTable,
    RepositoryLocationsTable,
)
from ursula.user_code.workspace import dagster_cloud_api_call


@pytest.fixture(name="cloud_api_daemon")
def cloud_api_daemon_fixture():
    return DagsterCloudApiDaemon()


@pytest.fixture(name="user_code_launcher")
def user_code_launcher_fixture(agent_instance):
    user_code_launcher = agent_instance.user_code_launcher

    yield user_code_launcher


@pytest.fixture(name="workspace")
def dynamic_workspace_fixture(user_code_launcher):
    with DynamicWorkspace(user_code_launcher) as workspace:
        yield workspace


@pytest.fixture(name="cloud_storage")
def cloud_storage_fixture(host_instance):
    cloud_storage = host_instance.cloud_storage

    yield cloud_storage

    with cloud_storage.transaction() as conn:
        conn.execute(RepositoryLocationsDataTable.delete())
        conn.execute(RepositoryLocationsTable.delete())


@pytest.fixture(name="user_cloud_agent_request_storage")
def user_agent_request_storage_fixture(host_instance):
    user_cloud_agent_request_storage = host_instance.user_cloud_agent_request_storage

    yield user_cloud_agent_request_storage

    user_cloud_agent_request_storage.wipe()


@op
def success():
    pass


@graph
def success_graph():
    success()


@repository
def repo():
    return [success_graph.to_job(name="success_job")]


def test_initial_run_iteration_populates_workspace(
    cloud_api_daemon,
    agent_instance,
    workspace,
    cloud_storage,
):
    location_name = "location"
    cloud_storage.add_location(
        location_name,
        deployment_metadata=CodeDeploymentMetadata(python_file=__file__),
    )
    repository_location_origin = RegisteredRepositoryLocationOrigin(location_name)

    with pytest.raises(Exception):
        workspace.get_location(repository_location_origin)

    next(cloud_api_daemon.run_iteration(agent_instance, workspace))
    workspace.grpc_server_registry.reconcile()

    assert workspace.get_location(repository_location_origin)


def test_repeated_run_iteration_populates_workspace_only_once(
    cloud_api_daemon,
    agent_instance,
    workspace,
    cloud_storage,
):
    location_name_one = "location1"
    cloud_storage.add_location(
        location_name_one,
        deployment_metadata=CodeDeploymentMetadata(python_file=__file__),
    )
    repository_location_origin_one = RegisteredRepositoryLocationOrigin(location_name_one)

    next(cloud_api_daemon.run_iteration(agent_instance, workspace))

    location_name_two = "location2"
    cloud_storage.add_location(
        location_name_two,
        deployment_metadata=CodeDeploymentMetadata(python_file=__file__),
    )
    repository_location_origin_two = RegisteredRepositoryLocationOrigin(location_name_two)

    next(cloud_api_daemon.run_iteration(agent_instance, workspace))
    workspace.grpc_server_registry.reconcile()

    assert workspace.get_location(repository_location_origin_one)

    with pytest.raises(Exception):
        workspace.get_location(repository_location_origin_two)


def test_check_for_workspace_updates(
    cloud_api_daemon,
    agent_instance,
    workspace,
    cloud_storage,
    user_cloud_agent_request_storage,
):
    location_name_one = "location1"
    cloud_storage.add_location(
        location_name_one,
        deployment_metadata=CodeDeploymentMetadata(python_file=__file__),
    )
    repository_location_origin_one = RegisteredRepositoryLocationOrigin(location_name_one)

    next(cloud_api_daemon.run_iteration(agent_instance, workspace))

    location_name_two = "location2"
    cloud_storage.add_location(
        location_name_two,
        deployment_metadata=CodeDeploymentMetadata(python_file=__file__),
    )
    repository_location_origin_two = RegisteredRepositoryLocationOrigin(location_name_two)

    dagster_cloud_api_call(
        user_cloud_agent_request_storage,
        DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
        wait_for_response=False,
    )

    next(cloud_api_daemon.run_iteration(agent_instance, workspace))
    workspace.grpc_server_registry.reconcile()

    assert workspace.get_location(repository_location_origin_one)
    assert workspace.get_location(repository_location_origin_two)
