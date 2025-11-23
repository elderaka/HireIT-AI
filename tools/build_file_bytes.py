from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Optional
import json

@tool
def build_file_bytes(
    text: str,
    ext: str = "txt",
    encoding: str = "utf-8"
) -> bytes:
    """
    Convert text into raw file bytes for export/upload.
    
    Args:
        text: The content to write.
        ext: Desired file type hint. Supports txt/md/json/csv. Defaults to txt.
        encoding: Text encoding. Defaults to utf-8.
        
    Returns:
        bytes: Raw bytes representing the file.
    """
    e = ext.lower().strip()

    if e in ("txt", "md", "csv"):
        return text.encode(encoding)

    if e == "json":
        # If text is valid JSON, pretty-print it.
        # Otherwise wrap it into {"content": "..."}.
        try:
            obj = json.loads(text)
        except Exception:
            obj = {"content": text}
        pretty = json.dumps(obj, ensure_ascii=False, indent=2)
        return pretty.encode(encoding)

    return text.encode(encoding)
