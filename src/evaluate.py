from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_tickets.csv"
OUTPUT_PATH = ROOT / "data" / "evaluation_results.csv"

sys.path.append(str(ROOT / "src"))

from classify_ticket import classify_ticket  # noqa: E402


def calculate_accuracy(df: pd.DataFrame, actual_col: str, predicted_col: str) -> float:
    if df.empty:
        return 0.0

    correct = (df[actual_col].astype(str) == df[predicted_col].astype(str)).sum()
    return round((correct / len(df)) * 100, 2)


def evaluate() -> pd.DataFrame:
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
    results = tickets.merge(prediction_df, on="ticket_id")

    print("\nOpsOracle evaluation")
    print("====================")
    print(f"Tickets evaluated: {len(results)}")
    print(f"Type accuracy: {calculate_accuracy(results, 'true_type', 'predicted_type')}%")
    print(f"Priority accuracy: {calculate_accuracy(results, 'true_priority', 'predicted_priority')}%")
    print(f"Assignment group accuracy: {calculate_accuracy(results, 'suggested_group', 'predicted_group')}%")
    print(f"Security flag accuracy: {calculate_accuracy(results, 'security_flag', 'predicted_security_flag')}%")

    print("\nPredicted assignment groups")
    print("===========================")
    print(results["predicted_group"].value_counts())

    print("\nPredicted priorities")
    print("====================")
    print(results["predicted_priority"].value_counts())

    print("\nSecurity flagged tickets")
    print("========================")
    security_tickets = results[results["predicted_security_flag"] == True]
    if security_tickets.empty:
        print("No security tickets flagged.")
    else:
        print(security_tickets[["ticket_id", "title", "predicted_priority", "predicted_group"]])

    results.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved detailed results to {OUTPUT_PATH}")

    return results


if __name__ == "__main__":
    evaluate()