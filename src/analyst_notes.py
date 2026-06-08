from __future__ import annotations

from typing import Dict


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def generate_analyst_note(ticket: Dict[str, object]) -> str:
    security_flag = parse_bool(ticket.get("predicted_security_flag", False))

    note_parts = [
        f"Ticket {ticket.get('ticket_id')} has been classified as {ticket.get('predicted_type')} with priority {ticket.get('predicted_priority')}.",
        f"The recommended assignment group is {ticket.get('predicted_group')}.",
        f"Reasoning: {ticket.get('evidence')}",
    ]

    if security_flag:
        note_parts.append(
            "Security risk has been flagged. Recommended next step is to review sign-in logs, recent account activity, and any related alerts before resolution."
        )
    else:
        note_parts.append(
            "No immediate security indicator was detected from the ticket text."
        )

    resolution_hint = ticket.get("resolution_hint")

    if resolution_hint:
        note_parts.append(f"Suggested resolution path: {resolution_hint}")

    note_parts.append(
        "This recommendation should be reviewed by an analyst before action is taken."
    )

    return " ".join(note_parts)

def get_analyst_note(ticket: Dict[str, object]) -> tuple[str, bool]:
    """Returns (note_text, is_ai_generated)."""
    try:
        from llm_notes import generate_llm_note
        note = generate_llm_note(ticket)
        return note, True
    except Exception:
        return generate_analyst_note(ticket), False