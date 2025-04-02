class IpActionTest:
    def test_ip_reputation(self, client, app_id, ip_artifact):
        """Test ip reputation"""
        result = client.run_action(
            name="Test action",
            action="ip reputation",
            container_id=ip_artifact["container_id"],
            targets=[
                {
                    "app_id": app_id,
                    "assets": [app_id],
                    "parameters": [{"ip": "4.4.4.4"}],
                }
            ],
        )
        assert result["riskscore"] == 0
        assert result["rulecount"] == 0
        assert result["name"] == "4.4.4.4"

    def test_ip_intelligence(self, client, app_id, ip_artifact):
        """Test ip intelligence"""
        result = client.run_action(
            name="Test action",
            action="ip intelligence",
            container_id=ip_artifact["container_id"],
            targets=[
                {
                    "app_id": app_id,
                    "assets": [app_id],
                    "parameters": [{"ip": "4.4.4.4"}],
                }
            ],
        )
        expected_keys = [
            "risk",
            "entity",
            "location",
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
