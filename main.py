from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import uuid

app = FastAPI()
OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

class GenerateFileReq(BaseModel):
    text: str
    filename: str | None = None  # optional
    ext: str = "txt"

@app.post("/generate-file")
def generate_file(req: GenerateFileReq):
    fname = req.filename or f"hireit_{uuid.uuid4().hex}.{req.ext}"
    path = OUT_DIR / fname
    path.write_text(req.text, encoding="utf-8")
    # Local demo: return path. If you add storage later, return URL.
    return {"ok": True, "filename": fname, "local_path": str(path)}
