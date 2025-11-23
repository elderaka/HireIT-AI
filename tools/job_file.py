import ast
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, List, Union
import re, json, base64

KEYS = [
    "Job Title",
    "Department",
    "Location",
    "Employment Type",
    "Seniority",
    "Deadline",
    "Owner Email",
    "Requirements",
    "Nice-to-have",
    "Notes",
]

def _normalize_newlines(text: str) -> str:
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    if "\\n" in t and "\n" not in t:
        t = t.replace("\\n", "\n")
    return t.strip()

def _extract_blocks(text: str) -> Dict[str, str]:
    key_pattern = "|".join(re.escape(k) for k in KEYS)
    pattern = re.compile(
        rf"(?P<key>{key_pattern})\s*:\s*(?P<val>.*?)(?=\n(?:{key_pattern})\s*:|$)",
        re.DOTALL | re.IGNORECASE,
    )
    out: Dict[str, str] = {}
    for m in pattern.finditer(text):
        raw_key = m.group("key").strip()
        val = m.group("val").strip()
        canon = next(k for k in KEYS if k.lower() == raw_key.lower())
        out[canon] = val
    return out

def _split_list(val: str) -> List[str]:
    if not val:
        return []
    items = re.split(r"[;\n•\-\*]+", val)
    return [i.strip() for i in items if i.strip()]

def _clean_title(title: str) -> str:
    t = re.sub(r"[\r\n:]+", " ", title).strip()
    return t[:80]

@tool
def normalize_job_intake(filled_text: str) -> Dict[str, Any]:
    """Normalize a filled job intake template into structured JSON."""
    text = _normalize_newlines(filled_text)
    blocks = _extract_blocks(text)

    job_title = blocks.get("Job Title", "")
    department = blocks.get("Department", "")
    location = blocks.get("Location", "")
    employment_type = blocks.get("Employment Type", "")
    seniority = blocks.get("Seniority", "")
    deadline = blocks.get("Deadline", "")
    owner_email = blocks.get("Owner Email", "")
    requirements = _split_list(blocks.get("Requirements", ""))
    nice_to_have = _split_list(blocks.get("Nice-to-have", ""))
    notes = blocks.get("Notes", "")

    warnings: List[str] = []
    if not job_title:
        warnings.append("job_title is empty.")
    if not owner_email:
        warnings.append("owner_email is empty.")

    title_clean = _clean_title(job_title) if job_title else ""

    return {
        "ok": True if job_title else False,
        "job_title": job_title,
        "department": department,
        "location": location,
        "employment_type": employment_type,
        "seniority": seniority,
        "deadline": deadline,
        "owner_email": owner_email,
        "requirements": requirements,
        "nice_to_have": nice_to_have,
        "notes": notes,
        "meta": {"warnings": warnings},
        "proposed_root_folder_name": f"{title_clean} Application" if title_clean else ""
    }
@tool
def build_text_bytes(content: str, file_name: str = "artifact.txt", encoding: str = "utf-8") -> Dict[str, Any]:
    """Build bytes for a text artifact (.txt/.json string/etc)."""
    b = (content or "").encode(encoding)
    return {
        "ok": True,
        "file_name": file_name,
        "file_type": file_name.split(".")[-1].lower() if "." in file_name else "txt",
        "content": content,
        "file_bytes": b,
        "file_bytes_b64": base64.b64encode(b).decode("ascii"),
        "meta": {"byte_len": len(b)}
    }
@tool

@tool
def build_json_bytes(data: Union[Dict[str, Any], str], file_name="job_intake.json", indent=2):
    """Build bytes for a JSON artifact (.json)."""
    try:
        indent = int(indent)
    except Exception:
        indent = 2

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = ast.literal_eval(data)

    json_str = json.dumps(data or {}, ensure_ascii=False, indent=indent)
    return build_text_bytes(content=json_str, file_name=file_name)