from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, List
import re

@tool
def normalize_job_intake(filled_text: str) -> Dict[str, Any]:
    """
    Normalize a filled Job Listing intake template into structured JSON.

    Expected input: lines like "Field: value". Fields are case-insensitive.
    Requirements / Nice-to-have may be bullets or semicolon/comma separated.

    Returns:
      {
        "job_title": str,
        "department": str,
        "location": str,
        "employment_type": str,
        "seniority": str,
        "deadline": str,
        "owner_email": str,
        "requirements": [str],
        "nice_to_have": [str],
        "notes": str,
        "proposed_root_folder_name": str,
        "meta": {"warnings":[...]}
      }
    """
    meta = {"warnings": []}

    lines = [ln.strip() for ln in (filled_text or "").splitlines() if ln.strip()]
    kv = {}
    current_key = None
    buf: List[str] = []

    field_map = {
        "job title": "job_title",
        "department": "department",
        "location": "location",
        "employment type": "employment_type",
        "seniority": "seniority",
        "deadline": "deadline",
        "owner email": "owner_email",
        "requirements": "requirements",
        "nice-to-have": "nice_to_have",
        "nice to have": "nice_to_have",
        "notes": "notes",
    }

    def flush():
        nonlocal current_key, buf
        if current_key:
            kv[current_key] = "\n".join(buf).strip()
        current_key = None
        buf = []

    for ln in lines:
        m = re.match(r"^([A-Za-z\-\s]+)\s*:\s*(.*)$", ln)
        if m:
            flush()
            raw_key = m.group(1).strip().lower()
            val = m.group(2).strip()
            current_key = field_map.get(raw_key)
            if current_key is None:
                current_key = raw_key.replace(" ", "_")
                meta["warnings"].append(f"Unknown field '{raw_key}' kept as '{current_key}'.")
            buf.append(val)
        else:
            if current_key is None:
                meta["warnings"].append(f"Unkeyed line ignored: '{ln[:50]}'")
                continue
            buf.append(ln)

    flush()

    def split_list(v: str) -> List[str]:
        if not v:
            return []
        parts = []
        for p in re.split(r"(?:\n|;|,|\u2022|\-|\*)+", v):
            p = p.strip()
            if p:
                parts.append(p)
        return parts

    out: Dict[str, Any] = {
        "job_title": kv.get("job_title", "").strip(),
        "department": kv.get("department", "").strip(),
        "location": kv.get("location", "").strip(),
        "employment_type": kv.get("employment_type", "").strip(),
        "seniority": kv.get("seniority", "").strip(),
        "deadline": kv.get("deadline", "").strip(),
        "owner_email": kv.get("owner_email", "").strip(),
        "requirements": split_list(kv.get("requirements", "")),
        "nice_to_have": split_list(kv.get("nice_to_have", "")),
        "notes": kv.get("notes", "").strip(),
        "meta": meta,
    }

    if not out["job_title"]:
        meta["warnings"].append("job_title is empty.")
    if not out["owner_email"]:
        meta["warnings"].append("owner_email is empty.")

    out["proposed_root_folder_name"] = (
        f"{out['job_title']} Application".strip() if out["job_title"] else "Application"
    )

    return out
