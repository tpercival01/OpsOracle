# OpsOracle

OpsOracle is an AI-assisted incident triage and IT automation prototype for support and operations teams.

It classifies synthetic ServiceNow-style tickets, predicts priority, identifies likely assignment groups, flags possible security risk, retrieves similar incidents, and generates analyst-style triage notes.

## Why this project exists

Support and application teams spend a lot of time triaging repetitive tickets, routing issues, checking priority, reviewing similar incidents, and writing analyst notes.

OpsOracle demonstrates how Python automation and applied AI-style workflows can improve triage consistency, reduce repetitive support work, and support faster operational decision-making.

## Current MVP

The current MVP includes:

- Synthetic ServiceNow-style ticket dataset
- Rule-based incident/request classifier
- Priority prediction
- Assignment group prediction
- Security risk flagging
- Confidence score
- Evidence explanation
- Similar ticket retrieval
- Analyst-style note generation
- Evaluation metrics
- Streamlit dashboard
- CSV export of triage results

## Stack

- Python
- pandas
- scikit-learn
- Streamlit
- TF-IDF similarity search
- Rule-based classification
- Synthetic IT support data

## Dataset fields

- ticket_id
- title
- description
- category
- affected_service
- user_department
- impact
- urgency
- true_type
- true_priority
- security_flag
- suggested_group
- resolution_hint

## Evaluation

The evaluation script compares predicted values against labelled synthetic data:

- true_type vs predicted_type
- true_priority vs predicted_priority
- suggested_group vs predicted_group
- security_flag vs predicted_security_flag

The project outputs evaluation metrics for:

- incident/request classification accuracy
- priority prediction accuracy
- assignment group prediction accuracy
- security flag detection accuracy

## Project purpose

This project is designed to demonstrate practical skills in:

- Application support workflow design
- IT support triage automation
- Incident and request classification
- Python automation
- Data processing with pandas
- Similarity search
- Evaluation-driven development
- Streamlit dashboarding
- Explainable operational decision support

## How it works

OpsOracle uses a labelled synthetic dataset of IT support tickets. Each ticket includes a title, description, affected service, impact, urgency, true ticket type, expected priority, security flag, suggested assignment group, and resolution hint.

The classifier applies transparent rule-based logic to each ticket and returns:

- predicted ticket type
- predicted priority
- predicted assignment group
- predicted security flag
- confidence score
- evidence explanation

The Streamlit dashboard displays the triage results, summary metrics, ticket filters, single-ticket analysis, analyst-style notes, similar previous tickets, and downloadable CSV output.

## Example use cases

OpsOracle is designed around common support and operations workflows such as:

- authentication and access issues
- Microsoft 365 and Exchange Online requests
- Intune and endpoint support
- suspicious login or phishing reports
- application and API incidents
- network and VPN issues
- collaboration platform requests
- support ticket routing and prioritisation

## Roadmap

Planned improvements:

- Add LLM-generated analyst notes
- Add synthetic ticket generator
- Add knowledge-base retrieval
- Add confidence thresholds and escalation logic
- Add ServiceNow-style dashboard metrics
- Add incident postmortem generation
- Add monitoring/log-style event triage
- Add deployment
- Add richer evaluation reporting
- Add screenshots and demo walkthrough

## Status

MVP in development.

The current focus is building a clean, working prototype that demonstrates support triage automation, explainable classification, evaluation metrics, and operational workflow thinking.