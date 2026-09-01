from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.process_service import ProcessService
from backend.schemas.process import ProcessCreate, ProcessResponse, ProcessListResponse
from typing import List, Optional

router = APIRouter()


@router.get("", response_model=List[ProcessListResponse])
def list_processes(
    business_function: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    svc = ProcessService(db)
    return svc.list_processes(business_function=business_function, skip=skip, limit=limit)


@router.post("", response_model=ProcessResponse, status_code=201)
def create_process(data: ProcessCreate, db: Session = Depends(get_db)):
    svc = ProcessService(db)
    return svc.create_process(data)


@router.get("/top", response_model=List[dict])
def top_processes(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    svc = ProcessService(db)
    return svc.get_top_processes(limit=limit)


@router.get("/human-led", response_model=List[dict])
def human_led_processes(db: Session = Depends(get_db)):
    svc = ProcessService(db)
    return svc.get_human_led_processes()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    svc = ProcessService(db)
    return svc.get_stats()


@router.get("/{process_id}", response_model=ProcessResponse)
def get_process(process_id: int, db: Session = Depends(get_db)):
    svc = ProcessService(db)
    proc = svc.get_process(process_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Process not found")
    return proc
