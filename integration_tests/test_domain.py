def test_domain_intelligence(run_action):
    result = run_action("domain intelligence", [{"domain": "google.com"}])
    expected_keys = [
        "risk",
        "entity",
        "intelCard",
        "mitreTags",
        "aiInsights",
        "timestamps",
        "ai_insights",
        "threatLists",
        "relatedEntities",
        "recordedfutureLinks",
    ]
    assert list(result.keys()) == expected_keys


def test_domain_reputation(run_action):
    result = run_action("domain reputation", [{"domain": "google.com"}])
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
