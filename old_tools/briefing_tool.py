from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, Optional
import re
import json

try:
    import requests  # type: ignore
except Exception:
    requests = None  # type: ignore


@tool
def get_public_text_or_json(link: str, ext: str = "txt", timeout_s: int = 20) -> Dict[str, Any]:
    """
    Download a public Google Drive FILE (not folder) and return text.
    Accepts:
      - https://drive.google.com/file/d/<id>/view?...
      - https://drive.google.com/uc?export=download&id=<id>
    Returns:
      { ok, file_id, file_type, text, obj, meta }
    """
    if not link:
        return {"ok": False, "error": "empty link"}

    # Extract file id from common patterns
    m = re.search(r"/file/d/([a-zA-Z0-9_-]+)", link)
    if not m:
        m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", link)

    file_id: Optional[str] = m.group(1) if m else None
    if not file_id and "drive.google.com/uc" not in link:
        return {
            "ok": False,
            "error": "not a Drive FILE link or download link",
            "meta": {"hint": "folders not supported, delegate DataHub first"}
        }

    # Build download url if needed
    download_url = link
    if file_id and "uc?export=download" not in link:
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    if requests is None:
        return {"ok": False, "error": "requests not available in runtime"}

    r = requests.get(download_url, timeout=timeout_s)
    r.raise_for_status()

    # Decode as text
    text = r.content.decode("utf-8", errors="replace").strip()

    obj = None
    warnings = []

    # If JSON-like, parse it
    if text.startswith("{") or text.startswith("["):
        try:
            obj = json.loads(text)
        except Exception as e:
            warnings.append(f"json_parse_failed: {e}")

    return {
        "ok": True,
        "file_id": file_id,
        "file_type": ext,
        "text": text,
        "obj": obj,                 # <-- never None if parse succeeds
        "meta": {"warnings": warnings, "download_url": download_url}
    }
