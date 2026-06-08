from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DATA_PATH = ROOT / "data" / "synthetic_tickets.csv"

sys.path.append(str(SRC))

from classify_ticket import classify_ticket 
from similarity import find_similar_tickets  
from analyst_notes import get_analyst_note  


st.set_page_config(
    page_title="OpsOracle",
    page_icon="🧠",
    layout="wide",
)

st.title("OpsOracle")
st.subheader("AI-assisted incident triage and IT automation prototype")

st.write(
    """
    OpsOracle classifies synthetic ServiceNow-style tickets, predicts priority,
    identifies likely assignment groups, flags possible security risks, retrieves
    similar incidents, and generates analyst-style triage notes.
    """
)

@st.cache_data
def load_results() -> pd.DataFrame:
    tickets = pd.read_csv(DATA_PATH)
    predictions = []
    for _, row in tickets.iterrows():
        prediction = classify_ticket(row.to_dict())
        predictions.append(
            {
                "ticket_id": row["ticket_id"],
                "predicted_type": prediction.predicted_type,
                "predicted_priority": prediction.predicted_priority,
                "predicted_group": prediction.predicted_group,
                "predicted_security_flag": prediction.predicted_security_flag,
                "confidence": prediction.confidence,
                "evidence": prediction.evidence,
            }
        )
    prediction_df = pd.DataFrame(predictions)
    return tickets.merge(prediction_df, on="ticket_id")


results = load_results()


def accuracy(actual_col: str, predicted_col: str) -> float:
    correct = (
        results[actual_col].astype(str)
        == results[predicted_col].astype(str)
    ).sum()

    return round((correct / len(results)) * 100, 2)


st.markdown("## Evaluation summary")

metric_col_1, metric_col_2, metric_col_3, metric_col_4, metric_col_5 = st.columns(5)

metric_col_1.metric("Tickets", len(results))
metric_col_2.metric("Type accuracy", f"{accuracy('true_type', 'predicted_type')}%")
metric_col_3.metric("Priority accuracy", f"{accuracy('true_priority', 'predicted_priority')}%")
metric_col_4.metric("Group accuracy", f"{accuracy('suggested_group', 'predicted_group')}%")
metric_col_5.metric("Security accuracy", f"{accuracy('security_flag', 'predicted_security_flag')}%")

st.divider()

chart_col_1, chart_col_2, chart_col_3 = st.columns(3)

with chart_col_1:
    st.markdown("### Predicted groups")
    group_counts = results["predicted_group"].value_counts()
    st.bar_chart(group_counts)

with chart_col_2:
    st.markdown("### Predicted priority")
    priority_counts = results["predicted_priority"].value_counts()
    st.bar_chart(priority_counts)

with chart_col_3:
    st.markdown("### Security flags")
    security_counts = results["predicted_security_flag"].astype(str).value_counts()
    st.bar_chart(security_counts)

st.divider()

st.markdown("## Ticket filters")

filter_col_1, filter_col_2, filter_col_3 = st.columns(3)

with filter_col_1:
    group_filter = st.selectbox(
        "Assignment group",
        ["All"] + sorted(results["predicted_group"].unique().tolist()),
    )

with filter_col_2:
    priority_filter = st.selectbox(
        "Priority",
        ["All"] + sorted(results["predicted_priority"].unique().tolist()),
    )

with filter_col_3:
    security_only = st.checkbox("Security flagged only")

filtered = results.copy()

if group_filter != "All":
    filtered = filtered[filtered["predicted_group"] == group_filter]

if priority_filter != "All":
    filtered = filtered[filtered["predicted_priority"] == priority_filter]

if security_only:
    filtered = filtered[filtered["predicted_security_flag"] == True]

st.markdown("## Triaged tickets")

display_columns = [
    "ticket_id",
    "title",
    "affected_service",
    "true_type",
    "predicted_type",
    "true_priority",
    "predicted_priority",
    "suggested_group",
    "predicted_group",
    "predicted_security_flag",
    "confidence",
    "evidence",
]

st.dataframe(filtered[display_columns], use_container_width=True)

csv_output = results.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download triage results as CSV",
    data=csv_output,
    file_name="opsoracle_triage_results.csv",
    mime="text/csv",
)

st.divider()

st.markdown("## Single ticket triage")

selected_ticket_id = st.selectbox(
    "Select ticket",
    results["ticket_id"].tolist(),
)

selected_ticket = results[results["ticket_id"] == selected_ticket_id].iloc[0]
selected_ticket_dict = selected_ticket.to_dict()

left, right = st.columns(2)

with left:
    st.markdown("### Ticket")
    st.write(f"**Title:** {selected_ticket['title']}")
    st.write(f"**Description:** {selected_ticket['description']}")
    st.write(f"**Affected service:** {selected_ticket['affected_service']}")
    st.write(f"**Department:** {selected_ticket['user_department']}")
    st.write(f"**Impact:** {selected_ticket['impact']}")
    st.write(f"**Urgency:** {selected_ticket['urgency']}")
    st.write(f"**Original category:** {selected_ticket['category']}")

with right:
    st.markdown("### OpsOracle prediction")
    st.write(f"**Type:** {selected_ticket['predicted_type']}")
    st.write(f"**Priority:** {selected_ticket['predicted_priority']}")
    st.write(f"**Assignment group:** {selected_ticket['predicted_group']}")
    st.write(f"**Security flag:** {selected_ticket['predicted_security_flag']}")
    st.write(f"**Confidence:** {selected_ticket['confidence']}")
    st.write(f"**Evidence:** {selected_ticket['evidence']}")

st.markdown("### Analyst note")

analyst_note, is_ai = get_analyst_note(selected_ticket_dict)

if is_ai:
    st.markdown("** AI Analyst Note**")
else:
    st.markdown("**Rule-based Analyst Note**")

st.info(analyst_note)

similar_tickets = find_similar_tickets(results, selected_ticket_id, top_n=3)

if similar_tickets:
    similar_df = pd.DataFrame(similar_tickets)
    similar_df["similarity"] = similar_df["similarity"].round(2)
    st.dataframe(similar_df, use_container_width=True)
else:
    st.write("No similar tickets found.")