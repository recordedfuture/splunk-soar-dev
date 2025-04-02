def test_file_intelligence(run_action):
    _hash = "f3c20ff70c1c69098bcacc8d6857d542661781851d68094d8aa9126a111ad541"
    result = run_action("file intelligence", [{"hash": _hash}])
    expected_keys = [
        "risk",
        "entity",
        "intelCard",
        "mitreTags",
        "aiInsights",
        "timestamps",
        "ai_insights",
        "threatLists",
        "hashAlgorithm",
        "relatedEntities",
        "recordedfutureLinks",
    ]
    assert list(result.keys()) == expected_keys


def test_file_reputation(run_action):
    _hash = "f3c20ff70c1c69098bcacc8d6857d542661781851d68094d8aa9126a111ad541"
    result = run_action("file reputation", [{"hash": _hash}])
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
