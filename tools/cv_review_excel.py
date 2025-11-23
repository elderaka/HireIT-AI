"""Utility tool for exporting CV review results to CSV.

Intended to be used as a Python tool in watsonx Orchestrate.
It converts a list of candidate review objects into a flat CSV table.
Can also parse agent response text to extract review data.
"""

from typing import List, Dict, Optional, Union
import csv
import os
import re
import json


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


def parse_agent_review_response(response_text: str) -> List[Dict]:
    """Parse agent's review response text into structured data.
    
    Extracts candidate information from formatted text like:
    1. **John Doe** - Score: 9/10
       - Skills: Python, Django
       - Experience: 6 years
       - Why: Strong match...
       - Missing: None
    
    Parameters
    ----------
    response_text : str
        The text response from Reviewer or Mass_Review agent
    
    Returns
    -------
    List[Dict]
        List of candidate objects with parsed data
    """
    candidates = []
    
    # Pattern to match candidate entries
    # Matches: 1. **Name** - Score: X/10
    pattern = r'\d+\.\s+\*\*(.+?)\*\*\s+-\s+Score:\s+(\d+(?:\.\d+)?)/10\s+(.+?)(?=\d+\.\s+\*\*|\Z)'
    
    matches = re.finditer(pattern, response_text, re.DOTALL)
    
    # Find section boundaries for decision detection
    sections = {
        'RECOMMEND': [],
        'CONSIDER': [],
        'REJECT': []
    }
    
    # Find all section headers and their positions
    recommend_pos = [m.start() for m in re.finditer(r'🟢\s+RECOMMENDED', response_text)]
    consider_pos = [m.start() for m in re.finditer(r'🟡\s+CONSIDER', response_text)]
    reject_pos = [m.start() for m in re.finditer(r'🔴\s+NOT\s+RECOMMENDED', response_text)]
    
    for match in matches:
        name = match.group(1).strip()
        score = float(match.group(2))
        details = match.group(3).strip()
        match_pos = match.start()
        
        # Extract details
        skills_match = re.search(r'-\s+Skills:\s+(.+?)(?=\n\s+-|\Z)', details)
        exp_match = re.search(r'-\s+Experience:\s+(.+?)(?=\n\s+-|\Z)', details)
        why_match = re.search(r'-\s+Why:\s+(.+?)(?=\n\s+-|\Z)', details)
        missing_match = re.search(r'-\s+Missing:\s+(.+?)(?=\n\s+-|\Z)', details)
        
        # Determine decision based on which section this candidate is in
        decision = 'CONSIDER'  # default
        
        # Check if match is after recommend section but before consider
        if recommend_pos and match_pos > recommend_pos[0]:
            decision = 'RECOMMEND'
            if consider_pos and match_pos > consider_pos[0]:
                decision = 'CONSIDER'
            if reject_pos and match_pos > reject_pos[0]:
                decision = 'REJECT'
        elif consider_pos and match_pos > consider_pos[0]:
            decision = 'CONSIDER'
            if reject_pos and match_pos > reject_pos[0]:
                decision = 'REJECT'
        elif reject_pos and match_pos > reject_pos[0]:
            decision = 'REJECT'
        else:
            # Fallback to score-based decision
            decision = 'RECOMMEND' if score >= 8 else 'CONSIDER' if score >= 6 else 'REJECT'
        
        candidate = {
            'name': name,
            'final_score': score,
            'auto_decision': decision,
            'skills': skills_match.group(1).strip() if skills_match else '',
            'experience': exp_match.group(1).strip() if exp_match else '',
            'reasoning': why_match.group(1).strip() if why_match else '',
            'missing': missing_match.group(1).strip() if missing_match else '',
        }
        
        candidates.append(candidate)
    
    return candidates


def export_review_summary_to_csv(
    agent_response: Union[str, List[Dict]],
    output_path: str = "review_summary.csv",
    job_title: Optional[str] = None
) -> str:
    """Export agent review response to CSV with full details.
    
    Parameters
    ----------
    agent_response : Union[str, List[Dict]]
        Either raw text response from agent or structured candidate list
    output_path : str, optional
        Path to the CSV file to be created
    job_title : str, optional
        Job title to include in the export
    
    Returns
    -------
    str
        The absolute path of the created CSV file
    """
    # Parse response if it's text
    if isinstance(agent_response, str):
        candidates = parse_agent_review_response(agent_response)
        # Try to extract job title from response
        if not job_title:
            job_match = re.search(r'Job:\s+(.+?)(?=\n|Total)', agent_response)
            if job_match:
                job_title = job_match.group(1).strip()
    else:
        candidates = agent_response
    
    if not candidates:
        raise ValueError("No candidates found in response")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    headers = [
        "Name",
        "Score",
        "Decision",
        "Skills",
        "Experience",
        "Reasoning",
        "Missing/Gaps",
        "Job Title"
    ]
    
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for c in candidates:
            row = [
                c.get("name", ""),
                c.get("final_score", ""),
                c.get("auto_decision", ""),
                c.get("skills", ""),
                c.get("experience", ""),
                c.get("reasoning", ""),
                c.get("missing", ""),
                job_title or ""
            ]
            writer.writerow(row)
    
    return os.path.abspath(output_path)


def create_review_summary_from_text(
    agent_response_text: str,
    output_csv_path: str = "review_summary.csv"
) -> Dict:
    """Convenience function: Parse agent response and export to CSV.
    
    Parameters
    ----------
    agent_response_text : str
        The full text response from Reviewer/Mass_Review agent
    output_csv_path : str, optional
        Path for the output CSV file
    
    Returns
    -------
    Dict
        {
            "csv_path": str,
            "total_candidates": int,
            "recommended": int,
            "consider": int,
            "reject": int,
            "candidates": List[Dict]
        }
    """
    candidates = parse_agent_review_response(agent_response_text)
    
    if not candidates:
        return {
            "error": "No candidates found in response text",
            "csv_path": None,
            "total_candidates": 0
        }
    
    csv_path = export_review_summary_to_csv(candidates, output_csv_path)
    
    # Count by decision
    stats = {
        'RECOMMEND': 0,
        'CONSIDER': 0,
        'REJECT': 0
    }
    
    for c in candidates:
        decision = c.get('auto_decision', '').upper()
        if decision in stats:
            stats[decision] += 1
    
    return {
        "csv_path": csv_path,
        "total_candidates": len(candidates),
        "recommended": stats['RECOMMEND'],
        "consider": stats['CONSIDER'],
        "reject": stats['REJECT'],
        "candidates": candidates
    }
