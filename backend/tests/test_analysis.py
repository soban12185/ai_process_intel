import pytest
from backend.services.analysis_service import AnalysisService
from backend.services.process_service import ProcessService
from backend.schemas.process import ProcessCreate


def test_get_analyses_empty(db_session, process):
    svc = AnalysisService(db_session)
    analyses = svc.get_analyses(process.id)
    assert analyses == []


def test_get_evidence_empty(db_session, process):
    svc = AnalysisService(db_session)
    evidence = svc.get_evidence(process.id)
    assert evidence["process_id"] == process.id
    assert evidence["total_sources"] == 0


def test_analyze_process_without_llm(db_session, process):
    svc = AnalysisService(db_session)
    result = svc.analyze_process(process.id)
    assert result is not None
    assert result.status == "completed"
    assert result.process_id == process.id

    analyses = svc.get_analyses(process.id)
    assert len(analyses) >= 1
