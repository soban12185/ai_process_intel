import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import engine, SessionLocal, Base
from backend.models.organization import Organization
from backend.models.process import Process
from backend.models.activity import ProcessActivity
from backend.services.research_service import ResearchService


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        org = db.query(Organization).first()
        if not org:
            org = Organization(
                name="NovaBank",
                industry="Banking",
                description="NovaBank - Fictional Banking Institution for AI Process Intelligence Challenge",
            )
            db.add(org)
            db.flush()
            print(f"Created organization: {org.name} (ID: {org.id})")
        else:
            print(f"Organization already exists: {org.name} (ID: {org.id})")

        existing_count = db.query(Process).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} processes. Skipping seed.")
            return

        seed_path = os.path.join(os.path.dirname(__file__), "banking_processes.json")
        with open(seed_path, "r") as f:
            processes_data = json.load(f)

        print(f"Loading {len(processes_data)} banking processes...")

        for i, proc_data in enumerate(processes_data):
            proc = Process(
                org_id=org.id,
                name=proc_data["name"],
                description=proc_data["description"],
                business_purpose=proc_data["business_purpose"],
                business_function=proc_data["business_function"],
                status="seeded",
            )
            db.add(proc)
            db.flush()

            activities = proc_data.get("activities", [])
            for j, act_name in enumerate(activities):
                activity = ProcessActivity(
                    process_id=proc.id,
                    name=act_name,
                    description=f"Step {j + 1} of {proc_data['name']}",
                    sequence_order=j + 1,
                )
                db.add(activity)

            if (i + 1) % 20 == 0:
                print(f"  Loaded {i + 1}/{len(processes_data)} processes...")

        db.commit()
        print(f"Successfully seeded {len(processes_data)} banking processes.")

        print("Seeding research sources...")
        research_svc = ResearchService(db)
        research_svc.seed_research_sources()
        print("Research sources seeded.")

        total = db.query(Process).count()
        from sqlalchemy import func
        functions = db.query(Process.business_function, func.count(Process.id)).group_by(Process.business_function).all()
        print(f"\nFinal count: {total} processes across {len(functions)} business functions:")
        for func_name, count in functions:
            print(f"  - {func_name}: {count} processes")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
