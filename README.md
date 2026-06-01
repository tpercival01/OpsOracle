# OpsOracle

OpsOracle is an AI-assisted incident triage and IT automation prototype for support and operations teams.

It classifies synthetic ServiceNow-style tickets, predicts priority, identifies likely assignment groups, flags possible security risk, and explains the triage decision.

## Why this project exists

Support teams spend large amounts of time triaging repetitive tickets, routing issues, checking priority, and writing analyst notes.

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
- Evaluation metrics
- Streamlit dashboard

## Stack

- Python
- pandas
- Streamlit
- scikit-learn
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

## Running locally

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Evaluation
PYTHONPATH = src python src/evaluate.py

The evaluation script compares predicted values against labelled synthetic data:

- true_type vs predicted_type
- true_priority vs predicted_priority
- suggested_group vs predicted_group
- security_flag vs predicted_security_flag

## Roadmap
- Add similarity search for previous incidents
- Add LLM-generated analyst notes
- Add confidence thresholds and escalation logic
- Add synthetic ticket generator
- Add knowledge-base retrieval
- Add ServiceNow-style dashboard metrics
- Add exportable incident reports