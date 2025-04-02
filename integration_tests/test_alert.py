def test_alert_lookup(run_action):
    result = run_action("alert lookup", [{"alert_id": "1ytolX"}])
    expected_keys = [
        "id",
        "url",
        "rule",
        "type",
        "title",
        "review",
        "entities",
        "evidence",
        "triggered",
        "ai_insights",
        "criticalityLabel",
    ]
    assert list(result.keys()) == expected_keys


def test_alert_rule_search(run_action):
    result = run_action("alert rule search", [{"rule_search": ""}])

    assert list(result[0].keys()) == ["id", "name"]


def test_alert_search(run_action):
    """Super slow, should we actually have a limit on amount alert fetched"""
    result = run_action("alert rule search", [{"rule_search": ""}])
    rule_id = result[0]["id"]
    result = run_action(
        "alert search", [{"rule_id": rule_id, "timeframe": "-24h to now"}]
    )

    assert list(result.keys()) == ["rule", "alerts"]


def test_alert_update(run_action):
    result = run_action(
        "alert update",
        [
            {
                "alert_id": "1ytolX",
                "alert_status": "New",
                "alert_note": "Hello world",
            }
        ],
    )
    expected_keys = [
        "id",
        "note",
        "title",
        "status",
        "reviewDate",
        "statusDate",
        "statusChangeBy",
    ]
    assert list(result.keys()) == expected_keys


def test_playbook_alerts_search(run_action):
    result = run_action("playbook alerts search", [{}])
    expected_keys = [
        "title",
        "status",
        "created",
        "updated",
        "category",
        "owner_id",
        "priority",
        "owner_name",
        "actions_taken",
        "organisation_id",
        "organisation_name",
        "playbook_alert_id",
        "owner_organisation_details",
    ]
    assert list(result[0].keys()) == expected_keys


def test_playbook_alert_details(run_action):
    result = run_action("playbook alerts search", [{}])
    alert_id = result[0]["playbook_alert_id"]
    result = run_action("playbook alert details", [{"alert_id": alert_id}])
    expected_keys = [
        "images",
        "category",
        "panel_log",
        "panel_log_v2",
        "panel_status",
        "playbook_alert_id",
        "panel_evidence_dns",
        "panel_evidence_whois",
        "panel_evidence_summary",
    ]

    assert list(result.keys()) == expected_keys


def test_update_playbook_alert(run_action):
    result = run_action("playbook alerts search", [{}])
    alert_id = result[0]["playbook_alert_id"]

    result = run_action(
        "playbook alert update",
        [
            {
                "alert_id": alert_id,
                "priority": "High",
                "status": "Pending",
                "log_message": "Hello world",
            }
        ],
    )
    assert list(result.keys()) == ["status"]
