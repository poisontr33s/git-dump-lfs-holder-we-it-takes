from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
import json

router = APIRouter()

SAVES_DIR = Path(__file__).resolve().parents[2] / "data" / "saves"
SAVES_DIR.mkdir(parents=True, exist_ok=True)

class SaveRequest(BaseModel):
    snapshot: Dict[str, Any]

class SaveResponse(BaseModel):
    ok: bool
    integrity: float
    timestamp: str
    filename: str

@router.post("/write", response_model=SaveResponse)
def write(req: SaveRequest):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"save_{ts}.json"
    path = SAVES_DIR / filename

    # Simple integrity metric: presence of core fields
    core_fields = ["player", "scene", "skills"]
    integrity = sum(1 for f in core_fields if f in req.snapshot) / len(core_fields)

    with path.open("w", encoding="utf-8") as f:
        json.dump({"timestamp": ts, "snapshot": req.snapshot}, f, indent=2)

    return SaveResponse(ok=True, integrity=round(float(integrity), 2), timestamp=datetime.utcnow().isoformat(), filename=filename)
