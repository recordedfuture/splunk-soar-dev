import json
from requests import Session
import requests
from typing import List, Literal
from time import sleep


LABELS = Literal["events", "incident", "intelligence", "vulnerability"]


def artifact(**kwargs):
    """Return a Phantom artifact with the supplied CEF fields."""
    artifact = {
        # "asset_id":10,
        # "cef_types": {
        #     "my_custom_cef_field": [ "ip" ]
        # },
        # "container_id": 100,
        # "data":{},
        # "end_time":"2014-10-19T14:45:51.100Z",
        "label": "event",
        "run_automation": True,
        # "severity":"high",
        # "source_data_identifier":"4",
        # "start_time":"2014-10-19T14:41:33.384Z",
        # "tags": ["tag1", "tag2"],
        # "type":"network"
    }
    artifact["cef"] = kwargs
    return artifact


def container(event_name="Test event", artifacts=[], tag="test"):
    """Return a Phantom container with the supplied fields."""
    return {
        # "asset_id": 12,
        "artifacts": artifacts,
        "custom_fields": {},
        # "data": { },
        "description": "Test container.",
        # "due_time": "2015-03-21T19:29:23.759Z",
        "label": "events",
        "name": event_name,
        # "owner_id": "phantom@recordedfuture.com",
        # "run_automation": True,
        # "sensitivity": "red",
        # "severity": "high",
        # "source_data_identifier": "4",
        # "status": "new",
        # "start_time": "2015-03-21T19:28:13.759Z",
        # "open_time": "2015-03-21T19:29:00.141Z",
        "tags": [tag],
    }


def target(app_id: int, assets: List[int], parameters: List[dict]):
    return [{"app_id": app_id, "assets": assets, "parameters": parameters}]


class PhantomClient:
    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.session = Session()
        self.base_url = f"https://{host}/rest"

    def call(self, method, path, payload=None):
        resp = self.session.request(
            method=method,
            url=f"{self.base_url}{path}",
            data=json.dumps(payload),
            headers={"ph-auth-token": self.token},
            verify=False,
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            raise ValueError(e.response.text)
        return resp.json()

    def get(self, path):
        return self.call("GET", path=path)

    def post(self, path, payload):
        return self.call("POST", path=path, payload=payload)

    def delete(self, path):
        return self.call("DELETE", path=path)

    def run_action(
        self,
        name: str,
        action: str,
        container_id: int,
        targets: List[dict],
        options: dict = {},
    ):
        """
        See https://docs.splunk.com/Documentation/SOAR/current/PlatformAPI/RESTRunAction
        for full list of post parameters
        """
        data = {
            "action": action,
            "container_id": container_id,
            "name": name,
            "targets": targets,
            **options,
        }
        resp = self.post("/action_run", payload=data)
        action_id = resp["action_run_id"]
        app_run_id = self._get_app_run(action_id)
        return self.app_run(app_run_id)

    def _get_app_run(self, _id: int):
        return self.get(f"/action_run/{_id}/app_runs")["data"][0]["id"]

    def create_container(self, name: str, label: LABELS, options: dict):
        """
        See https://docs.splunk.com/Documentation/SOAR/current/PlatformAPI/RESTContainers
        for full list post parameters
        """
        data = options
        data.update({"name": name, "label": label})
        return self.post("/container", payload=data)

    def app_run(self, _id: int):
        data = self.get(f"/app_run/{_id}/action_result")["data"]
        while len(data) == 0:
            sleep(0.1)
            data = self.get(f"/app_run/{_id}/action_result")["data"]
        if data[0]["status"] == "failed":
            raise ValueError(data[0]["message"])
        if len(data[0]["data"]) > 1:
            return data[0]["data"]
        return data[0]["data"][0]

    def delete_container(self, _id):
        return self.delete(f"/container/{_id}")

    def app_status(self):
        return self.get("/app_status")
