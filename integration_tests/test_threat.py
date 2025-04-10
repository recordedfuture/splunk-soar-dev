import pytest


def test_threat_map(run_action):
    result = run_action("threat map", [])
    expected_keys = ["threatActor"]
    assert list(result.keys()) == expected_keys


def test_threat_assessment(run_action):
    result = run_action("threat assessment", [{"threat_context": "c2"}])
    expected_keys = ["context", "verdict", "entities", "triage_riskscore"]
    assert list(result.keys()) == expected_keys


def test_threat_actor_intelligence(run_action):
    result = run_action("threat actor intelligence", [{"threat_actor": "Killnet", "links": False}])
    expected_keys = [
        "id",
        "name",
        "alias",
        "intent",
        "location",
        "severity",
        "intelCard",
        "categories",
        "opportunity",
    ]
    assert list(result.keys()) == expected_keys
