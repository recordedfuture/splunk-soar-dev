import pytest


@pytest.mark.skip
def test_collective_insights_submit(run_action):
    """Do we want to submit collective insights in our test env"""
    result = run_action("collective insights submit", [{"rule_search": ""}])

    assert list(result[0].keys()) == ["id", "name"]


def test_detection_rule_search(run_action):
    result = run_action(
        "detection rule search",
        [{"entity_name": "8.8.8.8", "entity_type": "IpAddress"}],
    )
    expected_keys = [
        "id",
        "type",
        "rules",
        "title",
        "created",
        "updated",
        "description",
    ]

    assert list(result[0].keys()) == expected_keys


def test_links_search(run_action):
    result = run_action(
        "links search",
        [{"entity_name": "8.8.8.8", "entity_type": "IpAddress"}],
    )

    assert list(result.keys()) == ["links", "entity"]
