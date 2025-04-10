"""Test data to be used in test calls and assertions"""


# Response in the result_data objects data property for reputation actions
# when we pass a value not existing in RF
def testdata_reputation_wo_risk(entity, category):
    """Create result for entities wo known risk."""
    prefix = {
        "ip": "ip:",
        "domain": "idn:",
        "hash": "hash:",
        "vulnerability": "",
        "url": "url:",
    }[category]
    ctype = {
        "ip": "IpAddress",
        "domain": "InternetDomainName",
        "hash": "Hash",
        "vulnerability": "CyberVulnerability",
        "url": "URL",
    }[category]
    rules_per_category = {
        "ip": 51,
        "domain": 22,
        "hash": 0,
        "vulnerability": 22,
        "url": 0,
    }[category]
    res = [
        {
            "id": "%s%s" % (prefix, entity),
            "name": "%s" % entity,
            "type": ctype,
            "risklevel": 0,
            "riskscore": 0,
            "rulecount": 0,
            "maxrules": rules_per_category,
            "description": None,
            "evidence": [],
        }
    ]
    # currently only used for IP addresses vulnerability rules: 22, domain: 36

    return (res, "Risklevel: 0.0, Type: IpAddress, Riskscore: 0.0")


def testdata_reputation_na(entity, category):
    """Create result for entities that don't exist."""
    maxrules = {"ip": 51, "domain": 42, "hash": 12, "vulnerability": 0, "url": 27}[category]
    r_type, i_type = {
        "ip": ("IpAddress", "ip"),
        "domain": ("InternetDomainName", "idn"),
        "hash": ("Hash", "hash"),
        "url": ("URL", "url"),
    }.get(category, ("UNDEF", "undef"))

    r_msg = {"vulnerability": "Riskscore: No information available."}.get(category, r"Risk score: 0.0, Risk summary: 0 rules triggered of \d+")
    return (
        [
            {
                "evidence": [],
                "id": "%s:%s" % (i_type, entity),
                "name": entity,
                "type": r_type,
                "risklevel": 0,
                "riskscore": 0,
                "rulecount": 0,
                "maxrules": maxrules,
                "description": None,
            }
        ],
        r_msg,
    )


# Response in the result_data object's data property for intelligence actions
# when we pass a value not existing in RF

# FILE
testdata_404_intelligence_file = {
    "data": [
        {
            "threatLists": [],
            "risk": {
                "riskSummary": "No information available.",
                "criticality": None,
                "rules": None,
                "riskString": "",
                "score": None,
                "criticalityLabel": "None",
                "evidenceDetails": [],
            },
            "entity": {"name": "", "id": None, "type": None},
            "metrics": [],
            "intelCard": "",
            "timestamps": {"lastSeen": "never", "firstSeen": "never"},
            "relatedEntities": [],
        }
    ],
    "message": "Risksummary: No information available., Criticalitylabel: None, Lastseen: never",
}

# DOMAIN
testdata_404_intelligence_domain = testdata_404_intelligence_file

# URL
testdata_404_intelligence_url = {
    "data": [
        {
            "metrics": [],
            "timestamps": {"lastSeen": "never", "firstSeen": "never"},
            "relatedEntities": [],
            "risk": {
                "riskSummary": "No information available.",
                "criticality": None,
                "rules": None,
                "riskString": "",
                "score": None,
                "criticalityLabel": "None",
                "evidenceDetails": [],
            },
            "entity": {"name": "", "id": None, "type": None},
        }
    ],
    "message": "Risksummary: No information available., Criticalitylabel: None, Lastseen: never",
}

testdata_404_intelligence_vulnerability = {
    "data": [
        {
            "threatLists": [],
            "risk": {
                "riskSummary": "No information available.",
                "criticality": None,
                "rules": None,
                "riskString": "",
                "score": None,
                "criticalityLabel": "None",
                "evidenceDetails": [],
            },
            "entity": {"name": "", "id": None, "type": None},
            "metrics": [],
            "intelCard": "",
            "timestamps": {"lastSeen": "never", "firstSeen": "never"},
            "relatedEntities": [],
        }
    ],
    "message": "Risksummary: No information available., Criticalitylabel: None, Lastseen: never",
}

testdata_404_intelligence_ip = {
    "data": [
        {
            "threatLists": [],
            "risk": {
                "riskSummary": "No information available.",
                "criticality": None,
                "rules": None,
                "riskString": "",
                "score": None,
                "criticalityLabel": "None",
                "evidenceDetails": [],
            },
            "entity": {"name": "", "id": None, "type": None},
            "metrics": [],
            "intelCard": "",
            "location": {},
            "timestamps": {"lastSeen": "never", "firstSeen": "never"},
            "relatedEntities": [],
        }
    ],
    "message": "Risksummary: No information available., Criticalitylabel: None, Lastseen: never",
}
