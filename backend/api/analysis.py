from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.process import ProcessCreate
from backend.schemas.analysis import AnalysisResponse, AnalysisTriggerResponse
from backend.services.analysis_service import AnalysisService
from backend.services.process_service import ProcessService
from typing import List

router = APIRouter()


@router.post("/{process_id}/analyze", response_model=AnalysisTriggerResponse)
def analyze_process(process_id: int, db: Session = Depends(get_db)):
    svc = AnalysisService(db)
    result = svc.analyze_process(process_id)
    if not result:
        raise HTTPException(status_code=404, detail="Process not found")
    return result


@router.get("/{process_id}/analysis", response_model=List[AnalysisResponse])
def get_analysis(process_id: int, db: Session = Depends(get_db)):
    svc = AnalysisService(db)
    analyses = svc.get_analyses(process_id)
    return analyses


@router.get("/{process_id}/evidence")
def get_evidence(process_id: int, db: Session = Depends(get_db)):
    svc = AnalysisService(db)
    evidence = svc.get_evidence(process_id)
    return evidence


@router.post("/analyze-new", response_model=AnalysisTriggerResponse)
def analyze_new_process(data: ProcessCreate, db: Session = Depends(get_db)):
    proc_svc = ProcessService(db)
    proc = proc_svc.create_process(data)
    analysis_svc = AnalysisService(db)
    return analysis_svc.analyze_process(proc.id)
