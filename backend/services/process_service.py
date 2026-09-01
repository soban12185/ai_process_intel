from sqlalchemy.orm import Session
from backend.models.process import Process
from backend.models.activity import ProcessActivity
from backend.models.score import ProcessScore
from backend.models.analysis import ProcessAnalysis
from backend.schemas.process import ProcessCreate
from typing import List, Optional


class ProcessService:
    def __init__(self, db: Session):
        self.db = db

    def list_processes(self, business_function: Optional[str] = None, skip: int = 0, limit: int = 200) -> List[Process]:
        q = self.db.query(Process)
        if business_function:
            q = q.filter(Process.business_function == business_function)
        return q.order_by(Process.id).offset(skip).limit(limit).all()

    def get_process(self, process_id: int) -> Optional[Process]:
        return self.db.query(Process).filter(Process.id == process_id).first()

    def create_process(self, data: ProcessCreate) -> Process:
        from backend.models.organization import Organization
        org = self.db.query(Organization).first()
        if not org:
            org = Organization(name="NovaBank", industry="Banking", description="NovaBank - Fictional Banking Institution")
            self.db.add(org)
            self.db.flush()

        proc = Process(
            org_id=org.id,
            name=data.name,
            description=data.description,
            business_purpose=data.business_purpose,
            business_function=data.business_function,
            status="user_added",
        )
        self.db.add(proc)
        self.db.flush()

        for i, act in enumerate(data.activities):
            activity = ProcessActivity(
                process_id=proc.id,
                name=act.name,
                description=act.description,
                sequence_order=act.sequence_order or i + 1,
            )
            self.db.add(activity)

        self.db.commit()
        self.db.refresh(proc)
        return proc

    def get_top_processes(self, limit: int = 10) -> List[dict]:
        results = (
            self.db.query(Process, ProcessScore)
            .join(ProcessAnalysis, Process.id == ProcessAnalysis.process_id)
            .join(ProcessScore, ProcessAnalysis.id == ProcessScore.analysis_id)
            .order_by(ProcessScore.total_score.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "rank": i + 1,
                "process_id": p.id,
                "process_name": p.name,
                "business_function": p.business_function,
                "total_score": round(s.total_score, 1),
                "priority": s.priority,
                "automation_potential": _score_to_label(s.automation_potential),
                "business_benefit": _score_to_label(s.business_benefit),
                "risk_factor": _score_to_label(s.risk_factor),
            }
            for i, (p, s) in enumerate(results)
        ]

    def get_human_led_processes(self) -> List[dict]:
        results = (
            self.db.query(Process, ProcessScore, ProcessAnalysis)
            .join(ProcessAnalysis, Process.id == ProcessAnalysis.process_id)
            .join(ProcessScore, ProcessAnalysis.id == ProcessScore.analysis_id)
            .all()
        )
        human_led = []
        for p, s, a in results:
            reasons = []
            if s.regulatory_sensitivity >= 7:
                reasons.append("High regulatory sensitivity")
            if s.risk_factor >= 7:
                reasons.append("High decision risk")
            if s.automation_potential <= 4:
                reasons.append("Low automation feasibility")
            if "human judgment" in (a.human_involvement or "").lower() if isinstance(a.human_involvement, str) else False:
                reasons.append("Requires human judgment")

            high_risk = s.regulatory_sensitivity >= 7 or s.risk_factor >= 7
            low_auto = s.automation_potential <= 4
            if high_risk or low_auto:
                human_led.append({
                    "process_id": p.id,
                    "process_name": p.name,
                    "business_function": p.business_function,
                    "automation_potential": _score_to_label(s.automation_potential),
                    "regulatory_sensitivity": _score_to_label(s.regulatory_sensitivity),
                    "risk_factor": _score_to_label(s.risk_factor),
                    "reasons": reasons if reasons else ["Complex process requiring human oversight"],
                })
        return sorted(human_led, key=lambda x: x["regulatory_sensitivity"], reverse=True)

    def get_stats(self) -> dict:
        total = self.db.query(Process).count()
        analyzed = (
            self.db.query(Process.id)
            .join(ProcessAnalysis, Process.id == ProcessAnalysis.process_id)
            .distinct()
            .count()
        )

        scores = self.db.query(ProcessScore).all()
        if not scores:
            return {
                "total_processes": total,
                "analyzed_processes": analyzed,
                "very_high_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0,
                "avg_score": 0,
                "high_automation_count": 0,
            }

        priorities = {"Very High": 0, "High": 0, "Medium": 0, "Low": 0}
        high_auto = 0
        total_score = 0.0
        for s in scores:
            priorities[s.priority] = priorities.get(s.priority, 0) + 1
            if s.automation_potential >= 7:
                high_auto += 1
            total_score += s.total_score

        return {
            "total_processes": total,
            "analyzed_processes": analyzed,
            "very_high_count": priorities["Very High"],
            "high_count": priorities["High"],
            "medium_count": priorities["Medium"],
            "low_count": priorities["Low"],
            "avg_score": round(total_score / len(scores), 1) if scores else 0,
            "high_automation_count": high_auto,
        }


def _score_to_label(score: float) -> str:
    if score >= 8:
        return "Very High"
    elif score >= 6:
        return "High"
    elif score >= 4:
        return "Medium"
    else:
        return "Low"
