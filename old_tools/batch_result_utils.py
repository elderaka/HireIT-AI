"""Tools for packaging CV review results into a standard JSON structure.

These tools are meant to be used as Python tools in watsonx Orchestrate.
They do not perform LLM reasoning; they only organize already-evaluated data.
"""

from typing import List, Dict, Any


def build_batch_review_result(
    rubric_info: Dict[str, Any],
    candidates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Build a standardized batch review result object.

    Parameters
    ----------
    rubric_info : dict
        Dictionary with summary information about the rubric, for example:
        {
            "role_title": "Junior Backend Engineer",
            "threshold_score": 6.5,
            "salary_budget": {
                "currency": "IDR",
                "min": 8000000,
                "max": 12000000
            }
        }

    candidates : list of dict
        List of candidate dictionaries. Each candidate is expected to contain:
        - "file_name" (str)
        - "name" (str or None)
        - "email" (str or None)
        - "phone" (str or None)
        - "experience_years" (float or None)
        - "unreadable" (bool)
        - "unreadable_reason" (str or None)
        - "scores" (dict with at least "final_score")
        - "auto_decision" ("pass" | "borderline" | "fail")
        - "worth_range" (dict with "currency", "min", "max")
        - "evidence_bullets" (list of strings)

    Returns
    -------
    dict
        A JSON-serializable dictionary with the following top-level keys:
        - "rubric_info"
        - "candidates"
        - "excel_export" (with "columns" and "rows")
        - "supervisor_summary"
    """
    threshold = rubric_info.get("threshold_score", 0.0)
    salary_budget = rubric_info.get("salary_budget", {}) or {}

    # Build excel_export section
    columns = [
        "file_name",
        "name",
        "final_score",
        "auto_decision",
        "worth_min",
        "worth_max",
        "unreadable",
        "unreadable_reason",
    ]
    rows = []

    below_threshold = []
    outside_budget = []
    unreadable_files = []

    for c in candidates or []:
        scores = c.get("scores") or {}
        final_score = scores.get("final_score", c.get("final_score", 0.0))
        worth = c.get("worth_range") or {}
        file_name = c.get("file_name", "")

        row = [
            file_name,
            c.get("name", ""),
            final_score,
            c.get("auto_decision", ""),
            worth.get("min", ""),
            worth.get("max", ""),
            c.get("unreadable", False),
            c.get("unreadable_reason", ""),
        ]
        rows.append(row)

        # Suggested disqualification buckets
        if c.get("unreadable", False):
            unreadable_files.append(file_name)

        try:
            if float(final_score) < float(threshold):
                below_threshold.append(file_name)
        except Exception:
            # If no numeric score, skip threshold comparison
            pass

        # Outside budget (if worth_range clearly outside salary_budget)
        try:
            budget_min = float(salary_budget.get("min", 0))
            budget_max = float(salary_budget.get("max", 0))
            worth_min = float(worth.get("min", budget_min))
            worth_max = float(worth.get("max", budget_max))
            if worth_min < budget_min or worth_max > budget_max:
                outside_budget.append(file_name)
        except Exception:
            # If parsing fails, ignore for this heuristic
            pass

    excel_export = {
        "columns": columns,
        "rows": rows,
    }

    # Simple supervisor summary text
    role_title = rubric_info.get("role_title", "the role")
    total = len(candidates or [])
    passes = sum(1 for c in candidates or [] if c.get("auto_decision") == "pass")
    borderlines = sum(1 for c in candidates or [] if c.get("auto_decision") == "borderline")
    fails = sum(1 for c in candidates or [] if c.get("auto_decision") == "fail")

    summary_text = (
        f"Reviewed {total} candidate(s) for {role_title}. "
        f"Suggested passes: {passes}, borderlines: {borderlines}, fails: {fails}."
    )

    supervisor_summary = {
        "language": "en",
        "text": summary_text,
        "suggested_disqualifications": {
            "below_threshold": below_threshold,
            "outside_budget": outside_budget,
            "unreadable": unreadable_files,
        },
    }

    result = {
        "rubric_info": rubric_info,
        "candidates": candidates,
        "excel_export": excel_export,
        "supervisor_summary": supervisor_summary,
    }
    return result
