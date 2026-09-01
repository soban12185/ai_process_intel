import pytest
from backend.scoring.opportunity_scorer import calculate_score, label_to_score, WEIGHTS


def test_label_to_score():
    assert label_to_score("Very High") == 9.0
    assert label_to_score("High") == 7.5
    assert label_to_score("Medium") == 5.0
    assert label_to_score("Low") == 3.0
    assert label_to_score("unknown") == 5.0


def test_calculate_score_high():
    dims = {
        "automation_potential": 9.0,
        "business_benefit": 9.0,
        "data_availability": 8.0,
        "ai_feasibility": 9.0,
        "process_repetition": 8.0,
        "risk_factor": 2.0,
        "regulatory_sensitivity": 2.0,
    }
    result = calculate_score(dims)
    assert result["total_score"] > 60
    assert result["priority"] in ["High", "Very High"]


def test_calculate_score_low():
    dims = {
        "automation_potential": 2.0,
        "business_benefit": 3.0,
        "data_availability": 2.0,
        "ai_feasibility": 2.0,
        "process_repetition": 2.0,
        "risk_factor": 8.0,
        "regulatory_sensitivity": 9.0,
    }
    result = calculate_score(dims)
    assert result["total_score"] < 30
    assert result["priority"] in ["Low", "Medium"]


def test_calculate_score_medium():
    dims = {
        "automation_potential": 5.0,
        "business_benefit": 5.0,
        "data_availability": 5.0,
        "ai_feasibility": 5.0,
        "process_repetition": 5.0,
        "risk_factor": 5.0,
        "regulatory_sensitivity": 5.0,
    }
    result = calculate_score(dims)
    assert 25 <= result["total_score"] <= 50
    assert result["priority"] == "Medium"


def test_calculate_score_with_labels():
    dims = {
        "automation_potential": "High",
        "business_benefit": "High",
        "data_availability": "Medium",
        "ai_feasibility": "High",
        "process_repetition": "Medium",
        "risk_factor": "Low",
        "regulatory_sensitivity": "Low",
    }
    result = calculate_score(dims)
    assert result["total_score"] > 0
    assert result["priority"] in ["Medium", "High", "Very High"]


def test_scoring_formula_contains_all_dimensions():
    dims = {k: 5.0 for k in WEIGHTS}
    result = calculate_score(dims)
    for dim in WEIGHTS:
        assert dim in result["scoring_formula"]


def test_score_bounds():
    dims = {k: 10.0 for k in WEIGHTS}
    result = calculate_score(dims)
    assert result["total_score"] <= 100.0

    dims = {k: 0.0 for k in WEIGHTS}
    result = calculate_score(dims)
    assert result["total_score"] >= 0.0
