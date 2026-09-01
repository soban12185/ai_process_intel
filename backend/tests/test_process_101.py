import pytest
from backend.services.process_service import ProcessService
from backend.services.analysis_service import AnalysisService
from backend.schemas.process import ProcessCreate


def test_create_and_analyze_new_process(db_session, org):
    proc_svc = ProcessService(db_session)
    data = ProcessCreate(
        name="Insurance Claim Processing",
        description="Process insurance claims from filing through settlement",
        business_purpose="Settle insurance claims efficiently",
        business_function="Operations",
        activities=[
            {"name": "Receive claim", "sequence_order": 1},
            {"name": "Verify coverage", "sequence_order": 2},
            {"name": "Assess damage", "sequence_order": 3},
            {"name": "Process payment", "sequence_order": 4},
        ],
    )
    proc = proc_svc.create_process(data)
    assert proc.id is not None
    assert proc.name == "Insurance Claim Processing"
    assert proc.status == "user_added"

    procs = proc_svc.list_processes()
    assert any(p.name == "Insurance Claim Processing" for p in procs)


def test_new_process_has_activities(db_session, org):
    proc_svc = ProcessService(db_session)
    data = ProcessCreate(
        name="Supply Chain Finance",
        description="Finance supply chain operations",
        business_purpose="Provide working capital",
        business_function="Corporate Banking",
        activities=[
            {"name": "Onboard supplier", "sequence_order": 1},
            {"name": "Verify invoices", "sequence_order": 2},
            {"name": "Disburse funds", "sequence_order": 3},
        ],
    )
    proc = proc_svc.create_process(data)
    activities = db_session.query(
        __import__("backend.models.activity", fromlist=["ProcessActivity"]).ProcessActivity
    ).filter_by(process_id=proc.id).all()
    assert len(activities) == 3
    assert activities[0].name == "Onboard supplier"


def test_process_101_in_stats(db_session, org):
    proc_svc = ProcessService(db_session)
    data = ProcessCreate(
        name="Tokenization Service",
        description="Tokenize payment credentials",
        business_purpose="Enable secure payments",
        business_function="Payments",
    )
    proc = proc_svc.create_process(data)
    stats = proc_svc.get_stats()
    assert stats["total_processes"] >= 1
