from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from app.services.predictor import SimplePredictor

router = APIRouter()

class DialogueRequest(BaseModel):
    state: Dict[str, Any] = {}
    input: str

class DialogueResponse(BaseModel):
    text: str
    branches: Dict[str, str]
    checks: Dict[str, float]
    scenarios: list

predictor = SimplePredictor()

@router.post("/respond", response_model=DialogueResponse)
def respond(req: DialogueRequest):
    scenarios = predictor.scenarios(req.state)

    base_text = f"Astrid: 'I heard you, darling — {req.input}. The Steamworks hums.'"
    branches = {"probe": "Ask about the Obscura"}

    # Minimal skill check demo
    sensual = float(req.state.get("skills", {}).get("sensual_intelligence", 0.5))
    if predictor.skill_check(sensual, 0.55):
        branches["flirt"] = "Lean closer (Sensual Check: success path)"
        base_text += " Her smile sharpens; the air thickens."
    else:
        base_text += " A cool distance settles between you."

    checks = {"sensual_intelligence": sensual, "obscura_sensitivity": float(req.state.get("skills", {}).get("obscura_sensitivity", 0.5))}

    return DialogueResponse(text=base_text, branches=branches, checks=checks, scenarios=scenarios)
