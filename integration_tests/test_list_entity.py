"""Relating to lists etc"""

import pytest


@pytest.fixture(scope="session")
def list_id(run_action):
    return run_action("list search", [{}])[0]["id"]


def test_list_create(run_action):
    result = run_action(
        "create list",
        [
            {
                "list_name": "My list",
                "entity_types": "ip",
            }
        ],
    )

    expected = [
        "id",
        "name",
        "type",
        "created",
        "updated",
        "owner_id",
        "owner_name",
        "organisation_id",
        "organisation_name",
    ]

    assert list(result.keys()) == expected


def test_entity_search(run_action):
    result = run_action(
        "entity search",
        [
            {
                "name": "8.8.8.8",
                "entity_type": "IpAddress",
            }
        ],
    )
    expected_keys = ["id", "name", "type"]
    assert list(result[0].keys()) == expected_keys


@pytest.mark.dependency(name="add_entity")
def test_list_add_entity(run_action, list_id):
    result = run_action(
        "list add entity",
        [
            {
                "list_id": list_id,
                "entity_name": "8.8.8.8",
                "entity_type": "IpAddress",
            }
        ],
    )

    assert list(result.keys()) == ["result"]


def test_list_contexts(run_action):
    result = run_action("list contexts", [])
    assert list(result[0].keys()) == ["name", "context", "datagroup"]


@pytest.mark.dependency(depends=["add_entity"], name="list_entities")
def test_list_entities(run_action, list_id):
    result = run_action("list entities", [{"list_id": list_id}])

    assert list(result[0].keys()) == ["added", "entity", "status", "context"]


@pytest.mark.dependency(depends=["add_entity", "list_entities"])
def test_list_remove_entity(run_action, list_id):
    result = run_action(
        "list remove entity",
        [{"list_id": list_id, "entity_name": "8.8.8.8", "entity_type": "IpAddress"}],
    )

    assert list(result.keys()) == ["result"]


def test_list_search(run_action):
    result = run_action("list search", [{}])
    expected_keys = [
        "id",
        "name",
        "type",
        "created",
        "updated",
        "owner_id",
        "owner_name",
        "organisation_id",
        "organisation_name",
        "owner_organisation_details",
    ]
    assert list(result[0].keys()) == expected_keys


def test_list_details(run_action, list_id):
    result = run_action("list details", [{"list_id": list_id}])
    expected_keys = [
        "id",
        "name",
        "type",
        "created",
        "updated",
        "owner_id",
        "owner_name",
        "organisation_id",
        "organisation_name",
        "owner_organisation_details",
    ]
    assert list(result.keys()) == expected_keys


def test_list_status(run_action, list_id):
    result = run_action("list status", [{"list_id": list_id}])

    assert list(result.keys()) == ["size", "status"]
