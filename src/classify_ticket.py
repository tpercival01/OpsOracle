from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict


@dataclass
class Prediction:
    predicted_type: str
    predicted_priority: str
    predicted_group: str
    predicted_security_flag: bool
    confidence: float
    evidence: str


SECURITY_KEYWORDS = [
    "suspicious",
    "phishing",
    "malware",
    "unknown location",
    "unexpected mfa",
    "admin consent",
    "forwarding rule",
    "defender",
    "compromised",
    "risky sign-in",
]

AUTH_KEYWORDS = [
    "password",
    "pingid",
    "mfa",
    "login",
    "log in",
    "access",
    "locked",
    "cannot access",
]

EMAIL_KEYWORDS = [
    "mailbox",
    "outlook",
    "exchange",
    "email",
    "distribution list",
    "shared mailbox",
]

ENDPOINT_KEYWORDS = [
    "laptop",
    "intune",
    "autopilot",
    "device",
    "printer",
    "windows",
    "endpoint",
]

NETWORK_KEYWORDS = [
    "vpn",
    "wi-fi",
    "wifi",
    "network",
    "dhcp",
    "dns",
]

APP_KEYWORDS = [
    "api",
    "application",
    "database",
    "report",
    "portal",
    "http 500",
    "integration",
    "permission error",
]

COLLAB_KEYWORDS = [
    "teams",
    "sharepoint",
    "channel",
    "meeting room",
]


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def normalise_text(*values: str) -> str:
    return " ".join(value or "" for value in values).lower()


def classify_ticket(row: Dict[str, str]) -> Prediction:
    text = normalise_text(row.get("title", ""), row.get("description", ""))

    predicted_type = "Incident"
    predicted_priority = "P3"
    predicted_group = "Service Desk"
    security_flag = False
    confidence = 0.55
    evidence = "Default support triage classification."

    if contains_any(text, SECURITY_KEYWORDS):
        security_flag = True
        predicted_group = "Security Operations"
        predicted_type = "Incident"
        confidence = 0.9
        evidence = "Security-related keyword detected."

        if contains_any(text, ["malware", "forwarding rule", "compromised", "defender"]):
            predicted_priority = "P1"
        else:
            predicted_priority = "P2"

        return Prediction(
            predicted_type,
            predicted_priority,
            predicted_group,
            security_flag,
            confidence,
            evidence,
        )

    if contains_any(text, AUTH_KEYWORDS):
        predicted_group = "Identity and Access"
        evidence = "Authentication or access-management keyword detected."
        confidence = 0.78

    elif contains_any(text, EMAIL_KEYWORDS):
        predicted_group = "Messaging"
        evidence = "Email or Exchange Online keyword detected."
        confidence = 0.78

    elif contains_any(text, ENDPOINT_KEYWORDS):
        predicted_group = "Endpoint Support"
        evidence = "Endpoint or device-management keyword detected."
        confidence = 0.76

    elif contains_any(text, NETWORK_KEYWORDS):
        predicted_group = "Network Support"
        evidence = "Network or connectivity keyword detected."
        confidence = 0.76

    elif contains_any(text, APP_KEYWORDS):
        predicted_group = "Application Support"
        evidence = "Application or integration keyword detected."
        confidence = 0.8

    elif contains_any(text, COLLAB_KEYWORDS):
        predicted_group = "Collaboration Support"
        evidence = "Collaboration platform keyword detected."
        confidence = 0.72

    request_patterns = [
        r"\brequest\b",
        r"\bnew starter\b",
        r"\bcreate\b",
        r"\badd user\b",
        r"\bneeds access\b",
        r"\bshared mailbox\b",
        r"\bdistribution list\b",
    ]

    if any(re.search(pattern, text) for pattern in request_patterns):
        predicted_type = "Request"
        predicted_priority = "P4"
        confidence = min(confidence + 0.08, 0.95)

    if contains_any(text, ["multiple users", "outage", "failing", "http 500"]):
        predicted_priority = "P2"
        confidence = min(confidence + 0.05, 0.95)

    return Prediction(
        predicted_type=predicted_type,
        predicted_priority=predicted_priority,
        predicted_group=predicted_group,
        predicted_security_flag=security_flag,
        confidence=round(confidence, 2),
        evidence=evidence,
    )