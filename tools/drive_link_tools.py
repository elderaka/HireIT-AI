"""
HireIT AI - Google Drive link utilities for watsonx Orchestrate ADK.

Import this file as a Python tool with:
  orchestrate tools import -k python -f tools/drive_link_tools.py

Tools inside:
- extract_drive_file_id(link): extract FILE id from common Drive/Docs URLs.
- make_drive_download_link(file_id): build a direct-download URL.
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Optional
import re
from urllib.parse import urlparse, parse_qs


_PATTERNS = [
    # https://drive.google.com/file/d/<id>/view
    re.compile(r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)"),
    # https://drive.google.com/drive/folders/<id>
    re.compile(r"drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)"),
    # https://docs.google.com/document/d/<id>/edit
    re.compile(r"docs\.google\.com/(?:document|spreadsheets|presentation)/d/([a-zA-Z0-9_-]+)"),
    # https://drive.google.com/uc?id=<id>...
    re.compile(r"drive\.google\.com/uc\?[^#]*\bid=([a-zA-Z0-9_-]+)"),
    # Any /d/<id> segment (fallback)
    re.compile(r"/d/([a-zA-Z0-9_-]+)"),
]


@tool
def extract_drive_file_id(link: str) -> Optional[str]:
    """
    Extract a Google Drive file/folder ID from a URL.

    Supports links like:
      - https://drive.google.com/file/d/<id>/view?...
      - https://drive.google.com/open?id=<id>
      - https://drive.google.com/uc?export=download&id=<id>
      - https://docs.google.com/document/d/<id>/edit
      - https://drive.google.com/drive/folders/<id>

    Args:
        link: Google Drive / Docs sharing URL.

    Returns:
        The extracted ID string, or None if not found.
    """
    if not link:
        return None

    s = link.strip()

    # 1) Quick regex patterns
    for pat in _PATTERNS:
        m = pat.search(s)
        if m:
            return m.group(1)

    # 2) Query param fallbacks
    try:
        parsed = urlparse(s)
        q = parse_qs(parsed.query or "")
        for key in ("id", "fileId", "folderId"):
            if key in q and q[key]:
                return q[key][0]
    except Exception:
        pass

    return None


@tool
def make_drive_download_link(file_id: str) -> Optional[str]:
    """
    Build a direct-download link for a Drive file ID.

    Note:
      - This does NOT bypass permissions.
      - Works for files that allow download to the current user / public.

    Args:
        file_id: A Drive file ID.

    Returns:
        Direct download URL, or None if file_id is empty.
    """
    if not file_id:
        return None
    fid = file_id.strip()
    return f"https://drive.google.com/uc?export=download&id={fid}"
