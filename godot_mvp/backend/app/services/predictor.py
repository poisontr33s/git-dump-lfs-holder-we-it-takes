from typing import Dict, Any, List
import random

class SimplePredictor:
    """Safe stand-in for Kausalitets-Arkitekten.
    Avoids importing broken modules; deterministic-ish outputs for MVP.
    """

    def scenarios(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        rng = random.Random(str(state))
        out = []
        for i, kind in enumerate(["optimistic", "realistic", "pessimistic"], start=1):
            out.append({
                "scenario_id": f"timeline_{i}",
                "kind": kind,
                "confidence": round(rng.uniform(0.66, 0.93), 2),
                "effects": {
                    "sensual_intelligence": round(rng.uniform(-0.05, 0.1), 2),
                    "obscura_sensitivity": round(rng.uniform(-0.03, 0.08), 2),
                }
            })
        return out

    def skill_check(self, skill: float, difficulty: float) -> bool:
        return (skill + random.uniform(-0.2, 0.2)) >= difficulty
