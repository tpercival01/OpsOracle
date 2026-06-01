from __future__ import annotations

from typing import List, Dict

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_ticket_text(row: pd.Series) -> str:
    return " ".join(
        [
            str(row.get("title", "")),
            str(row.get("description", "")),
            str(row.get("category", "")),
            str(row.get("affected_service", "")),
            str(row.get("resolution_hint", "")),
        ]
    )


def find_similar_tickets(
    tickets: pd.DataFrame,
    ticket_id: str,
    top_n: int = 3,
) -> List[Dict[str, object]]:
    if tickets.empty:
        return []

    if ticket_id not in tickets["ticket_id"].values:
        return []

    working_df = tickets.copy()
    working_df["search_text"] = working_df.apply(build_ticket_text, axis=1)

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(working_df["search_text"])

    target_index = working_df.index[working_df["ticket_id"] == ticket_id][0]
    similarities = cosine_similarity(vectors[target_index], vectors).flatten()

    working_df["similarity"] = similarities

    similar = (
        working_df[working_df["ticket_id"] != ticket_id]
        .sort_values("similarity", ascending=False)
        .head(top_n)
    )

    return similar[
        [
            "ticket_id",
            "title",
            "category",
            "affected_service",
            "suggested_group",
            "resolution_hint",
            "similarity",
        ]
    ].to_dict(orient="records")