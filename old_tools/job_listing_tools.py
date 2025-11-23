"""
Job Listing Tools for watsonx Orchestrate.

Import with:
  orchestrate tools import -k python -f tools/job_listing_tools.py
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, Optional, List
import json, re, datetime

_SCHEMA = {
  "type": "object",
  "required": [
    "job_id",
    "title",
    "department",
    "location",
    "employment_type",
    "seniority",
    "description",
    "responsibilities",
    "requirements",
    "created_at"
  ],
  "properties": {
    "job_id": {
      "type": "string"
    },
    "title": {
      "type": "string"
    },
    "department": {
      "type": "string"
    },
    "location": {
      "type": "object",
      "required": [
        "remote_type"
      ],
      "properties": {
        "city": {
          "type": "string"
        },
        "country": {
          "type": "string"
        },
        "remote_type": {
          "type": "string",
          "enum": [
            "onsite",
            "hybrid",
            "remote"
          ]
        }
      }
    },
    "employment_type": {
      "type": "string",
      "enum": [
        "full_time",
        "part_time",
        "internship",
        "contract"
      ]
    },
    "seniority": {
      "type": "string",
      "enum": [
        "intern",
        "junior",
        "mid",
        "senior",
        "lead"
      ]
    },
    "description": {
      "type": "string"
    },
    "responsibilities": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "requirements": {
      "type": "object",
      "required": [
        "must_have"
      ],
      "properties": {
        "must_have": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "nice_to_have": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "skills": {
      "type": "object",
      "properties": {
        "hard": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "soft": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "salary": {
      "type": "object",
      "properties": {
        "min": {
          "type": [
            "number",
            "null"
          ]
        },
        "max": {
          "type": [
            "number",
            "null"
          ]
        },
        "currency": {
          "type": [
            "string",
            "null"
          ]
        },
        "period": {
          "type": [
            "string",
            "null"
          ],
          "enum": [
            "monthly",
            "yearly",
            "null"
          ]
        }
      }
    },
    "application": {
      "type": "object",
      "properties": {
        "deadline": {
          "type": [
            "string",
            "null"
          ],
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "link": {
          "type": [
            "string",
            "null"
          ]
        },
        "contact_email": {
          "type": [
            "string",
            "null"
          ]
        }
      }
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "created_at": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    }
  }
}

REQUIRED_TOP = set(_SCHEMA.get("required", []))
ENUMS = {
    "employment_type": set(_SCHEMA["properties"]["employment_type"]["enum"]),
    "seniority": set(_SCHEMA["properties"]["seniority"]["enum"]),
    "remote_type": set(_SCHEMA["properties"]["location"]["properties"]["remote_type"]["enum"])
}

def _today() -> str:
    return datetime.date.today().isoformat()

@tool
def job_listing_schema() -> Dict[str, Any]:
    """Return the job listing JSON schema."""
    return {"schema": _SCHEMA}

@tool
def make_job_listing_json(input_message: str) -> Dict[str, Any]:
    """
    Extract job listing fields from user message using LLM at runtime.
    This tool is a thin wrapper: Orchestrate should fill the body with watsonx.ai.
    """
    return {
        "ok": False,
        "job_listing": None,
        "meta": {
            "warnings": ["LLM extraction not executed in tool sandbox. Run in Orchestrate with watsonx.ai enabled."],
            "errors": ["no_llm_runtime"]
        }
    }

def _is_date(s: Any) -> bool:
    if not isinstance(s, str): return False
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", s))

def _ensure_list(x) -> List[str]:
    if x is None: return []
    if isinstance(x, list): return [str(i) for i in x]
    return [str(x)]

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
    # real newlines first
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    # if it looks like escaped newlines survived, unescape them
    if "\\n" in t and "\n" not in t:
        t = t.replace("\\n", "\n")
    return t.strip()

def _extract_blocks(text: str) -> Dict[str, str]:
    """
    Extract each field as a non-greedy block up to the next key.
    Works even if some values span multiple words.
    """
    # Build a regex that captures each key's value until next key or end.
    # Example: Job Title: (capture...) Department: ...
    key_pattern = "|".join(re.escape(k) for k in KEYS)
    pattern = re.compile(
        rf"(?P<key>{key_pattern})\s*:\s*(?P<val>.*?)(?=\n(?:{key_pattern})\s*:|$)",
        re.DOTALL | re.IGNORECASE,
    )
    out = {}
    for m in pattern.finditer(text):
        key = m.group("key").strip()
        val = m.group("val").strip()
        # normalize key to canonical form
        canon = next(k for k in KEYS if k.lower() == key.lower())
        out[canon] = val
    return out

def _split_list(val: str) -> List[str]:
    if not val:
        return []
    # accept bullets or semicolons
    items = re.split(r"[;\n•\-\*]+", val)
    return [i.strip() for i in items if i.strip()]

@tool
def normalize_job_intake(filled_text: str) -> Dict[str, Any]:
    """Normalize filled job intake text into structured fields."""
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

    warnings = []
    if not job_title:
        warnings.append("job_title is empty.")
    if not owner_email:
        warnings.append("owner_email is empty.")

    return {
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
        "proposed_root_folder_name": (job_title[:80].replace("\n"," ").replace(":"," ").strip() + " Application") if job_title else ""
    }

@tool
def validate_job_listing_json(job_listing: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministically validate & normalize job_listing."""
    errors: List[str] = []
    warnings: List[str] = []
    jl = dict(job_listing or {})

    if not jl.get("created_at"):
        jl["created_at"] = _today()
        warnings.append("created_at was missing; set to today.")

    missing = [k for k in REQUIRED_TOP if not jl.get(k)]
    if missing:
        errors.append("missing_required_top: " + ", ".join(missing))

    loc = jl.get("location") or {}
    if not isinstance(loc, dict):
        errors.append("location must be object")
        loc = {}
    remote_type = loc.get("remote_type")
    if remote_type and remote_type not in ENUMS["remote_type"]:
        errors.append(f"location.remote_type invalid: {remote_type}")
    if "remote_type" not in loc:
        errors.append("missing_required: location.remote_type")
    jl["location"] = {
        "city": str(loc.get("city","")) if loc.get("city") is not None else "",
        "country": str(loc.get("country","")) if loc.get("country") is not None else "",
        "remote_type": remote_type
    }

    for k in ("employment_type","seniority"):
        v = jl.get(k)
        if v and v not in ENUMS[k]:
            errors.append(f"{k} invalid: {v}")

    jl["responsibilities"] = _ensure_list(jl.get("responsibilities"))
    req = jl.get("requirements") or {}
    if not isinstance(req, dict): req = {}
    req["must_have"] = _ensure_list(req.get("must_have"))
    req["nice_to_have"] = _ensure_list(req.get("nice_to_have"))
    jl["requirements"] = req

    skills = jl.get("skills") or {}
    if not isinstance(skills, dict): skills = {}
    skills["hard"] = _ensure_list(skills.get("hard"))
    skills["soft"] = _ensure_list(skills.get("soft"))
    jl["skills"] = skills

    jl["tags"] = _ensure_list(jl.get("tags"))

    app = jl.get("application") or {}
    if not isinstance(app, dict): app = {}
    if app.get("deadline") and not _is_date(app["deadline"]):
        errors.append("application.deadline must be YYYY-MM-DD or null")
    jl["application"] = app

    ok = len(errors) == 0
    return {"ok": ok, "errors": errors, "warnings": warnings, "job_listing": jl}
