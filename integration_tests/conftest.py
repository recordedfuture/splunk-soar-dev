import os
import pytest
from .client import PhantomClient, container, artifact


@pytest.fixture(scope="session")
def client():
    host = os.environ.get("PHOST")
    token = os.environ.get("PTOK")
    if not host or not token:
        raise ValueError("Missing PHOST or PTOK as env vars")

    return PhantomClient(host, token)


@pytest.fixture(scope="session")
def ip_artifact(client):
    data = container(artifacts=[artifact(dst="4.4.4.4")])
    result = client.create_container(name="Test event", label="events", options=data)
    container_id = result["id"]
    artifact_id = result["artifacts"][0]["id"]
    return {"container_id": container_id, "artifact_id": artifact_id}


@pytest.fixture(scope="session")
def run_action(client, ip_artifact, app_id):
    def _run_action(action, parameters):
        return client.run_action(
            name="Test action",
            action=action,
            container_id=ip_artifact["container_id"],
            targets=[{"app_id": app_id, "assets": [app_id], "parameters": parameters}],
        )

    return _run_action


@pytest.fixture(scope="session")
def app_id(client):
    result = client.app_status()
    apps = result["data"]
    try:
        rf_app = [a for a in apps if "Recorded Future For Splunk SOAR" in a["message"]][0]
    except Exception:
        raise ValueError("Our app is not configured")
    return rf_app["id"]
