from fastapi import APIRouter, Depends
from backend.database import get_db
from backend.schemas.query import QueryRequest, QueryResponse
from backend.services.query_service import QueryService
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_engine(req: QueryRequest, db: Session = Depends(get_db)):
    svc = QueryService(db)
    return svc.process_query(req.question)
