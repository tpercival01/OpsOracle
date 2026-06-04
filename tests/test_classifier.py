from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from classify_ticket import classify_ticket
from analyst_notes import generate_analyst_note


def make_ticket(title: str, description: str) -> dict:
    return {"title": title, "description": description}


def test_malware_is_p1_security_ops():
    result = classify_ticket(make_ticket("Malware alert", "Defender reports malware on user laptop"))
    assert result.predicted_priority == "P1"
    assert result.predicted_group == "Security Operations"
    assert result.predicted_security_flag is True


def test_phishing_is_p2_security_ops():
    result = classify_ticket(make_ticket("Phishing email", "User received suspicious phishing link"))
    assert result.predicted_priority == "P2"
    assert result.predicted_group == "Security Operations"
    assert result.predicted_security_flag is True


def test_new_starter_is_request_p4():
    result = classify_ticket(make_ticket("New starter access", "Manager requests account for new starter"))
    assert result.predicted_type == "Request"
    assert result.predicted_priority == "P4"


def test_api_500_is_application_support():
    result = classify_ticket(make_ticket("API failing", "Internal integration returns http 500 during sync"))
    assert result.predicted_group == "Application Support"


def test_vpn_routes_to_network():
    result = classify_ticket(make_ticket("VPN down", "User cannot connect to VPN from home"))
    assert result.predicted_group == "Network Support"


def test_analyst_note_includes_security_warning():
    ticket = {
        "ticket_id": "INC0001",
        "predicted_type": "Incident",
        "predicted_priority": "P1",
        "predicted_group": "Security Operations",
        "predicted_security_flag": True,
        "evidence": "Security keyword detected.",
        "resolution_hint": "Isolate device.",
    }
    note = generate_analyst_note(ticket)
    assert "Security risk has been flagged" in note


def test_analyst_note_no_false_positive_on_string_false():
    ticket = {
        "ticket_id": "INC0002",
        "predicted_type": "Incident",
        "predicted_priority": "P3",
        "predicted_group": "Messaging",
        "predicted_security_flag": "False",
        "evidence": "Email keyword detected.",
        "resolution_hint": None,
    }
    note = generate_analyst_note(ticket)
    assert "No immediate security indicator" in note