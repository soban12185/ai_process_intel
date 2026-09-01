from backend.models.score import ProcessScore
from backend.config import settings

WEIGHTS = {
    "automation_potential": 0.20,
    "business_benefit": 0.18,
    "data_availability": 0.15,
    "ai_feasibility": 0.15,
    "process_repetition": 0.12,
    "risk_factor": -0.10,
    "regulatory_sensitivity": -0.10,
}


LABEL_MAP = {
    "very high": 9.0,
    "high": 7.5,
    "medium": 5.0,
    "low": 3.0,
    "very low": 1.5,
}


def label_to_score(label: str) -> float:
    return LABEL_MAP.get(label.lower().strip(), 5.0)


def calculate_score(dimensions: dict) -> dict:
    raw = 0.0
    for dim, weight in WEIGHTS.items():
        val = dimensions.get(dim, 5.0)
        if isinstance(val, str):
            val = label_to_score(val)
        raw += val * weight

    total = max(0.0, min(100.0, (raw / 10.0) * 100.0))

    if total >= 75:
        priority = "Very High"
    elif total >= 50:
        priority = "High"
    elif total >= 25:
        priority = "Medium"
    else:
        priority = "Low"

    formula_parts = []
    for dim, weight in WEIGHTS.items():
        val = dimensions.get(dim, 5.0)
        if isinstance(val, str):
            val = label_to_score(val)
        formula_parts.append(f"{dim}({val}) * {weight}")
    formula = " + ".join(formula_parts) + f" = raw {round(raw, 2)} -> score {round(total, 1)}"

    return {
        "automation_potential": dimensions.get("automation_potential", 5.0) if isinstance(dimensions.get("automation_potential", 5.0), (int, float)) else label_to_score(dimensions.get("automation_potential", "medium")),
        "business_benefit": dimensions.get("business_benefit", 5.0) if isinstance(dimensions.get("business_benefit", 5.0), (int, float)) else label_to_score(dimensions.get("business_benefit", "medium")),
        "data_availability": dimensions.get("data_availability", 5.0) if isinstance(dimensions.get("data_availability", 5.0), (int, float)) else label_to_score(dimensions.get("data_availability", "medium")),
        "ai_feasibility": dimensions.get("ai_feasibility", 5.0) if isinstance(dimensions.get("ai_feasibility", 5.0), (int, float)) else label_to_score(dimensions.get("ai_feasibility", "medium")),
        "process_repetition": dimensions.get("process_repetition", 5.0) if isinstance(dimensions.get("process_repetition", 5.0), (int, float)) else label_to_score(dimensions.get("process_repetition", "medium")),
        "risk_factor": dimensions.get("risk_factor", 3.0) if isinstance(dimensions.get("risk_factor", 3.0), (int, float)) else label_to_score(dimensions.get("risk_factor", "low")),
        "regulatory_sensitivity": dimensions.get("regulatory_sensitivity", 3.0) if isinstance(dimensions.get("regulatory_sensitivity", 3.0), (int, float)) else label_to_score(dimensions.get("regulatory_sensitivity", "low")),
        "total_score": round(total, 1),
        "priority": priority,
        "scoring_formula": formula,
    }
