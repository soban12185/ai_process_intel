from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.process_service import ProcessService

router = APIRouter()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    svc = ProcessService(db)
    return svc.get_stats()
