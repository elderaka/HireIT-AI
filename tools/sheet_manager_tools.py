from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, Optional, List, Tuple
import re
import csv
from io import BytesIO, StringIO

try:
    import requests  # type: ignore
except Exception:
    requests = None  # type: ignore


@tool
def extract_drive_file_id(link: str) -> Dict[str, Any]:
    """
    Extract a Google Drive/Docs/Sheets file_id from a link.

    Returns: {"file_id": "<id>" | None}
    """
    if not link:
        return {"file_id": None}
    patterns = [
        re.compile(r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)"),
        re.compile(r"docs\.google\.com/(?:document|spreadsheets|presentation)/d/([a-zA-Z0-9_-]+)"),
        re.compile(r"drive\.google\.com/uc\?[^#]*\bid=([a-zA-Z0-9_-]+)"),
        re.compile(r"/d/([a-zA-Z0-9_-]+)"),
        re.compile(r"[?&]id=([a-zA-Z0-9_-]+)"),
    ]
    s = link.strip()
    for pat in patterns:
        m = pat.search(s)
        if m:
            return {"file_id": m.group(1)}
    return {"file_id": None}


@tool
def make_sheets_export_link(file_id: str, format: str = "csv", gid: int = 0) -> Dict[str, Any]:
    """
    Make a public export URL for a Google Sheet.

    format: "csv" (default) or "xlsx".
    gid: sheet tab id (0 by default).

    Returns: {"export_url": "<url>"}
    """
    fmt = (format or "csv").lower()
    if fmt not in ("csv", "xlsx"):
        fmt = "csv"
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format={fmt}&gid={gid}"
    return {"export_url": url}


@tool
def download_public_bytes(url: str, timeout_sec: int = 30) -> Dict[str, Any]:
    """
    Download bytes from a public URL (Sheets export or Drive download).

    Returns:
      {"http_code": int, "content_type": str|None, "file_bytes": bytes}
    """
    if requests is None:
        return {"http_code": 0, "content_type": None, "file_bytes": b""}

    r = requests.get(url, timeout=timeout_sec)
    return {
        "http_code": r.status_code,
        "content_type": r.headers.get("Content-Type"),
        "file_bytes": r.content or b""
    }


@tool
def sniff_html_interstitial(file_bytes: bytes) -> Dict[str, Any]:
    """
    Detect if downloaded bytes look like an HTML interstitial instead of real CSV/XLSX.

    Returns: {"html": bool, "head": str}
    """
    head = (file_bytes or b"")[:300].lstrip()
    try:
        head_txt = head.decode("utf-8", errors="replace").lower()
    except Exception:
        head_txt = ""
    is_html = head_txt.startswith("<!doctype html") or "<html" in head_txt or "google drive" in head_txt
    return {"html": bool(is_html), "head": head_txt[:200]}


@tool
def parse_csv_bytes(file_bytes: bytes, encoding: str = "utf-8", limit_rows: int = 5000) -> Dict[str, Any]:
    """
    Parse CSV bytes into table + rows (list of dicts).

    Returns:
      {
        "headers": [...],
        "table": [[...], ...],
        "rows": [{header: value, ...}, ...],
        "meta": {"row_count": n}
      }
    """
    text = file_bytes.decode(encoding, errors="replace")
    reader = csv.reader(StringIO(text))
    table: List[List[str]] = []
    for i, row in enumerate(reader):
        if i >= limit_rows:
            break
        table.append(row)

    headers = table[0] if table else []
    rows = []
    for r in table[1:]:
        obj = {}
        for j, h in enumerate(headers):
            obj[h] = r[j] if j < len(r) else ""
        rows.append(obj)

    return {
        "headers": headers,
        "table": table,
        "rows": rows,
        "meta": {"row_count": len(rows)}
    }


@tool
def apply_sheet_patch(rows: List[Dict[str, Any]], patch_spec: Any) -> Dict[str, Any]:
    """
    Apply a simple patch_spec over rows.

    patch_spec can be a single dict or a list of dicts.
    Supported ops: update, append, delete.

    Returns:
      {"rows": updated_rows, "meta": {"changes": int}}
    """
    if rows is None:
        rows = []
    patches = patch_spec if isinstance(patch_spec, list) else [patch_spec]
    changes = 0
    updated = list(rows)

    def match_where(row: Dict[str, Any], where: Dict[str, Any]) -> bool:
        for k, v in (where or {}).items():
            if str(row.get(k, "")) != str(v):
                return False
        return True

    for p in patches:
        if not isinstance(p, dict):
            continue
        op = p.get("op")
        if op == "update":
            where = p.get("where", {})
            sets = p.get("set", {})
            for row in updated:
                if match_where(row, where):
                    for k, v in sets.items():
                        row[k] = v
                    changes += 1

        elif op == "append":
            row = p.get("row")
            if isinstance(row, dict):
                updated.append(row)
                changes += 1

        elif op == "delete":
            where = p.get("where", {})
            before = len(updated)
            updated = [r for r in updated if not match_where(r, where)]
            changes += (before - len(updated))

    return {"rows": updated, "meta": {"changes": changes}}


@tool
def build_csv_bytes(rows: List[Dict[str, Any]], headers: Optional[List[str]] = None, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Build CSV bytes from rows + headers.

    If headers is None, infer from union of keys in order of first appearance.

    Returns:
      {"file_bytes": bytes, "headers": headers}
    """
    if rows is None:
        rows = []

    if headers is None:
        headers = []
        seen = set()
        for r in rows:
            for k in r.keys():
                if k not in seen:
                    headers.append(k)
                    seen.add(k)

    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(headers)
    for r in rows:
        writer.writerow([r.get(h, "") for h in headers])

    b = out.getvalue().encode(encoding)
    return {"file_bytes": b, "headers": headers}
