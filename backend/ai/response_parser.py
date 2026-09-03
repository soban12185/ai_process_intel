import json
import logging

logger = logging.getLogger(__name__)


def parse_analysis_response(raw: dict) -> dict:
    if "error" in raw:
        return _fallback_analysis()

    required_fields = [
        "business_purpose", "key_activities", "current_challenges",
        "ai_opportunities", "automation_potential", "technologies",
        "business_benefits", "risks", "reasoning", "confidence",
    ]

    for field in required_fields:
        if field not in raw:
            logger.warning(f"Missing field '{field}' in LLM response, using fallback")
            raw[field] = _fallback_analysis().get(field, "")

    if not isinstance(raw.get("key_activities"), list):
        raw["key_activities"] = [str(raw.get("key_activities", ""))]
    if not isinstance(raw.get("current_challenges"), list):
        raw["current_challenges"] = [str(raw.get("current_challenges", ""))]
    if not isinstance(raw.get("ai_opportunities"), list):
        raw["ai_opportunities"] = [str(raw.get("ai_opportunities", ""))]
    if not isinstance(raw.get("technologies"), list):
        raw["technologies"] = [str(raw.get("technologies", ""))]
    if not isinstance(raw.get("business_benefits"), list):
        raw["business_benefits"] = [str(raw.get("business_benefits", ""))]
    if not isinstance(raw.get("risks"), list):
        raw["risks"] = [str(raw.get("risks", ""))]
    if not isinstance(raw.get("human_involvement"), list):
        raw["human_involvement"] = [str(raw.get("human_involvement", "Human oversight required"))]

    valid_auto = ["Very High", "High", "Medium", "Low"]
    if raw["automation_potential"] not in valid_auto:
        raw["automation_potential"] = "Medium"

    try:
        raw["confidence"] = float(raw["confidence"])
        raw["confidence"] = max(0.0, min(1.0, raw["confidence"]))
    except (ValueError, TypeError):
        raw["confidence"] = 0.5

    scoring = raw.get("scoring_dimensions", {})
    for dim in ["automation_potential", "business_benefit", "data_availability",
                 "ai_feasibility", "process_repetition", "risk_factor", "regulatory_sensitivity"]:
        try:
            val = float(scoring.get(dim, 5.0))
            scoring[dim] = max(1.0, min(10.0, val))
        except (ValueError, TypeError):
            scoring[dim] = 5.0
    raw["scoring_dimensions"] = scoring

    return raw


def _fallback_analysis() -> dict:
    return {
        "business_purpose": "Analysis pending - AI service unavailable",
        "key_activities": ["Manual process execution"],
        "current_challenges": ["Unable to determine - AI service unavailable"],
        "ai_opportunities": ["Re-analyze when AI service is available"],
        "automation_potential": "Medium",
        "human_involvement": ["Manual execution required"],
        "technologies": [],
        "business_benefits": [],
        "risks": [],
        "reasoning": "Analysis could not be completed. The AI service (Groq) is not configured or unavailable. Please set GROQ_API_KEY in .env and restart.",
        "confidence": 0.0,
        "scoring_dimensions": {
            "automation_potential": 5.0,
            "business_benefit": 5.0,
            "data_availability": 5.0,
            "ai_feasibility": 5.0,
            "process_repetition": 5.0,
            "risk_factor": 5.0,
            "regulatory_sensitivity": 5.0,
        },
    }
