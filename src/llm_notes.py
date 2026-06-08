from __future__ import annotations

import os
from typing import Dict

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def generate_llm_note(ticket: Dict[str, object]) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not set in environment.")

    client = Groq(api_key=api_key)

    prompt = (
        f"You are an IT support analyst writing a triage note.\n\n"
        f"Ticket: {ticket.get('ticket_id')}\n"
        f"Title: {ticket.get('title', '')}\n"
        f"Description: {ticket.get('description', '')}\n"
        f"Type: {ticket.get('predicted_type')}\n"
        f"Priority: {ticket.get('predicted_priority')}\n"
        f"Assignment group: {ticket.get('predicted_group')}\n"
        f"Security flag: {ticket.get('predicted_security_flag')}\n"
        f"Classifier reasoning: {ticket.get('evidence')}\n"
        f"Resolution hint: {ticket.get('resolution_hint', 'N/A')}\n\n"
        f"Write a concise 3-5 sentence analyst note covering: what the issue is, "
        f"why it was classified this way, recommended next steps, and any escalation needed. "
        f"Do not use bullet points. Professional tone."
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()