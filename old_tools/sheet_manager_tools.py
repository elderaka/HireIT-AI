from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Any, Dict, List, Union
import csv, json, ast, re
from io import StringIO

def _coerce_rows(x: Union[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Accept rows as a native list[dict] or a JSON/Python-literal string."""
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        try:
            val = json.loads(x)
            if isinstance(val, list):
                return val
        except Exception:
            pass
        # Fallback for python-ish repr with single quotes
        val = ast.literal_eval(x)
        if not isinstance(val, list):
            raise ValueError("rows string did not parse to a list")
        return val
    raise TypeError("rows must be list[dict] or str")

def _coerce_headers(x: Union[str, List[str]]) -> List[str]:
    """Accept headers as a native list[str] or a JSON/Python-literal string."""
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        try:
            val = json.loads(x)
            if isinstance(val, list):
                return val
        except Exception:
            pass
        val = ast.literal_eval(x)
        if not isinstance(val, list):
            raise ValueError("headers string did not parse to a list")
        return val
    raise TypeError("headers must be list[str] or str")

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Any, Dict, List, Union, Tuple
import csv, json, ast
from io import StringIO

def _loads_maybe(x):
    if not isinstance(x, str):
        return x
    try:
        return json.loads(x)
    except Exception:
        return ast.literal_eval(x)

def _normalize(headers_in, rows_in) -> Tuple[List[str], List[Dict[str, Any]]]:
    headers = _loads_maybe(headers_in)
    rows = _loads_maybe(rows_in)

    # Case 1: already list[dict]
    if isinstance(rows, list) and (len(rows) == 0 or isinstance(rows[0], dict)):
        if not isinstance(headers, list) or not all(isinstance(h, str) for h in headers):
            # infer headers from union of keys
            keyset = []
            for r in rows:
                for k in r.keys():
                    if k not in keyset:
                        keyset.append(k)
            headers = keyset
        return headers, rows

    # Case 2: list[list]
    if isinstance(rows, list) and (len(rows) == 0 or isinstance(rows[0], list)):
        # 2-col key-value pairs => single dict row
        if len(rows) > 0 and all(len(r) == 2 for r in rows):
            d = {k: v for k, v in rows}
            headers = list(d.keys())
            return headers, [d]

        # first row is headers
        if len(rows) > 0 and not headers:
            headers = [str(x) for x in rows[0]]
            body = rows[1:]
        else:
            body = rows

        # map each row to dict by headers
        dict_rows = []
        for r in body:
            d = {}
            for i, h in enumerate(headers):
                d[h] = r[i] if i < len(r) else ""
            dict_rows.append(d)
        return headers, dict_rows

    raise TypeError("Unsupported rows format")

@tool
def build_csv(
    rows: Union[str, List[Dict[str, Any]], List[List[Any]]],
    headers: Union[str, List[str], None] = None,
    file_name: str = "output.csv",
    preview_rows: int = 5,
) -> Dict[str, Any]:
    """
    Build a CSV from rows + headers.
    - No base64, no bytes in JSON.
    - Returns csv_text for easy downstream handling.
    """

    headers_list, rows_list = _normalize(headers, rows)

    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=headers_list, extrasaction="ignore")
    writer.writeheader()
    for r in rows_list:
        writer.writerow({h: r.get(h, "") for h in headers_list})

    csv_text = buf.getvalue()

    preview = [headers_list]
    for r in rows_list[: max(int(preview_rows), 0)]:
        preview.append([r.get(h, "") for h in headers_list])

    return {
        "ok": True,
        "file_name": file_name,
        "file_type": "csv",
        "headers": headers_list,
        "rows": rows_list,
        "row_count": len(rows_list),
        "preview_table": preview,
        "csv_text": csv_text,
        "meta": {"warnings": []},
    }

@tool
def extract_drive_file_id(link: str) -> Dict[str, Any]:
    """Extract a Google Drive/Docs/Sheets file_id from a link."""
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
