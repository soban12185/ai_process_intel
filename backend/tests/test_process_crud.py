import pytest
from backend.services.process_service import ProcessService
from backend.schemas.process import ProcessCreate


def test_create_process(db_session, org):
    svc = ProcessService(db_session)
    data = ProcessCreate(
        name="New Test Process",
        description="A test process",
        business_purpose="Testing",
        business_function="Operations",
        activities=[{"name": "Step 1", "description": "First step", "sequence_order": 1}],
    )
    proc = svc.create_process(data)
    assert proc.id is not None
    assert proc.name == "New Test Process"
    assert proc.status == "user_added"
    assert proc.org_id == org.id


def test_list_processes(db_session, process):
    svc = ProcessService(db_session)
    procs = svc.list_processes()
    assert len(procs) >= 1
    assert any(p.name == "Test Loan Processing" for p in procs)


def test_get_process(db_session, process):
    svc = ProcessService(db_session)
    p = svc.get_process(process.id)
    assert p is not None
    assert p.name == "Test Loan Processing"


def test_get_process_not_found(db_session):
    svc = ProcessService(db_session)
    p = svc.get_process(99999)
    assert p is None


def test_list_processes_by_function(db_session, process):
    svc = ProcessService(db_session)
    procs = svc.list_processes(business_function="Lending")
    assert len(procs) >= 1
    assert all(p.business_function == "Lending" for p in procs)


def test_get_stats_empty(db_session):
    svc = ProcessService(db_session)
    stats = svc.get_stats()
    assert stats["total_processes"] == 0
    assert stats["analyzed_processes"] == 0
