import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.organization import Organization
from backend.models.process import Process
from backend.models.activity import ProcessActivity
from backend.models.analysis import ProcessAnalysis, AnalysisRun
from backend.models.score import ProcessScore
from backend.models.research import ResearchSource, EvidenceLink

TEST_DB_URL = "sqlite:///./data/test_modus_ai.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def org(db_session):
    o = Organization(name="TestBank", industry="Banking", description="Test")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def process(db_session, org):
    p = Process(
        org_id=org.id,
        name="Test Loan Processing",
        description="Test process for loan applications",
        business_purpose="Process loans",
        business_function="Lending",
        status="seeded",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p
