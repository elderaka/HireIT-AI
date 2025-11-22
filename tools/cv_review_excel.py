"""Utility tool for exporting CV review results to CSV.

Intended to be used as a Python tool in watsonx Orchestrate.
It converts a list of candidate review objects into a flat CSV table.
"""

from typing import List, Dict
import csv
import os


def export_cv_review_to_csv(
    candidates: List[Dict],
    output_path: str = "cv_review_results.csv"
) -> str:
    """Export a list of candidate profiles to a CSV file.

    Parameters
    ----------
    candidates : List[Dict]
        List of candidate profile objects. Each object is expected to contain:
        - "file_name" (optional)
        - "name"
        - "scores.final_score" or "final_score"
        - "auto_decision"
        - "worth_range" (dict with keys: currency, min, max)
        - "unreadable" (bool, optional)
        - "unreadable_reason" (str, optional)

    output_path : str, optional
        Path to the CSV file to be created. Relative paths will be created
        relative to the current working directory.

    Returns
    -------
    str
        The absolute path of the created CSV file.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    headers = [
        "file_name",
        "name",
        "final_score",
        "auto_decision",
        "worth_currency",
        "worth_min",
        "worth_max",
        "unreadable",
        "unreadable_reason",
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for c in candidates or []:
            worth = c.get("worth_range") or {}
            scores = c.get("scores") or {}
            final_score = scores.get("final_score", c.get("final_score", ""))
            row = [
                c.get("file_name", ""),
                c.get("name", ""),
                final_score,
                c.get("auto_decision", ""),
                worth.get("currency", ""),
                worth.get("min", ""),
                worth.get("max", ""),
                c.get("unreadable", False),
                c.get("unreadable_reason", ""),
            ]
            writer.writerow(row)

    return os.path.abspath(output_path)
