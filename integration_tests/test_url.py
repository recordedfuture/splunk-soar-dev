def test_url_reputation(run_action):
    result = run_action("url intelligence", [{"url": "https://www.example.com"}])
    expected_keys = [
        "risk",
        "entity",
        "mitreTags",
        "aiInsights",
        "timestamps",
        "ai_insights",
        "relatedEntities",
        "recordedfutureLinks",
    ]
    assert list(result.keys()) == expected_keys


def test_url_intelligence(run_action):
    result = run_action("url reputation", [{"url": "https://www.example.com"}])
    expected_keys = [
        "id",
        "name",
        "type",
        "evidence",
        "maxrules",
        "risklevel",
        "riskscore",
        "rulecount",
        "description",
    ]
    assert list(result.keys()) == expected_keys
