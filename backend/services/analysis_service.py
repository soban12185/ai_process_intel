import json
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models.analysis import ProcessAnalysis, AnalysisRun
from backend.models.score import ProcessScore
from backend.models.process import Process
from backend.models.activity import ProcessActivity
from backend.schemas.analysis import AnalysisResponse, AnalysisTriggerResponse
from backend.ai.llm_client import call_llm
from backend.ai.prompts import SYSTEM_PROMPT, ANALYSIS_USER_PROMPT
from backend.ai.response_parser import parse_analysis_response
from backend.scoring.opportunity_scorer import calculate_score
from backend.services.research_service import ResearchService

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_process(self, process_id: int) -> AnalysisTriggerResponse:
        proc = self.db.query(Process).filter(Process.id == process_id).first()
        if not proc:
            return None

        activities = (
            self.db.query(ProcessActivity)
            .filter(ProcessActivity.process_id == process_id)
            .order_by(ProcessActivity.sequence_order)
            .all()
        )
        activity_text = ", ".join([a.name for a in activities]) if activities else "None specified"

        user_prompt = ANALYSIS_USER_PROMPT.format(
            name=proc.name,
            description=proc.description,
            business_function=proc.business_function,
            activities=activity_text,
        )

        run = AnalysisRun(
            process_id=process_id,
            run_type="analyze",
            model_used=f"groq/{settings_model()}",
            status="running",
        )
        self.db.add(run)
        self.db.flush()

        raw = call_llm(SYSTEM_PROMPT, user_prompt)

        parsed = parse_analysis_response(raw)

        analysis = ProcessAnalysis(
            process_id=process_id,
            analysis_run_id=run.id,
            business_purpose=parsed.get("business_purpose", ""),
            key_activities=json.dumps(parsed.get("key_activities", [])),
            current_challenges=json.dumps(parsed.get("current_challenges", [])),
            ai_opportunities=json.dumps(parsed.get("ai_opportunities", [])),
            automation_potential=parsed.get("automation_potential", "Medium"),
            human_involvement=json.dumps(parsed.get("human_involvement", [])),
            technologies=json.dumps(parsed.get("technologies", [])),
            business_benefits=json.dumps(parsed.get("business_benefits", [])),
            risks=json.dumps(parsed.get("risks", [])),
            reasoning=parsed.get("reasoning", ""),
            confidence=parsed.get("confidence", 0.5),
        )
        self.db.add(analysis)
        self.db.flush()

        scoring_dims = parsed.get("scoring_dimensions", {})
        score_result = calculate_score(scoring_dims)

        score = ProcessScore(
            analysis_id=analysis.id,
            automation_potential=score_result["automation_potential"],
            business_benefit=score_result["business_benefit"],
            data_availability=score_result["data_availability"],
            ai_feasibility=score_result["ai_feasibility"],
            process_repetition=score_result["process_repetition"],
            risk_factor=score_result["risk_factor"],
            regulatory_sensitivity=score_result["regulatory_sensitivity"],
            total_score=score_result["total_score"],
            priority=score_result["priority"],
            scoring_formula=score_result["scoring_formula"],
        )
        self.db.add(score)

        run.status = "completed"
        run.completed_at = datetime.utcnow()
        self.db.commit()

        try:
            research_svc = ResearchService(self.db)
            research_svc.link_research(process_id, analysis.id, proc.name, proc.business_function)
        except Exception as e:
            logger.warning(f"Research enrichment failed: {e}")

        return AnalysisTriggerResponse(
            message="Analysis completed successfully",
            process_id=process_id,
            analysis_id=analysis.id,
            status="completed",
        )

    def get_analyses(self, process_id: int) -> list:
        analyses = (
            self.db.query(ProcessAnalysis)
            .filter(ProcessAnalysis.process_id == process_id)
            .order_by(ProcessAnalysis.created_at.desc())
            .all()
        )
        results = []
        for a in analyses:
            results.append(AnalysisResponse(
                id=a.id,
                process_id=a.process_id,
                business_purpose=a.business_purpose,
                key_activities=json.loads(a.key_activities) if a.key_activities else [],
                current_challenges=json.loads(a.current_challenges) if a.current_challenges else [],
                ai_opportunities=json.loads(a.ai_opportunities) if a.ai_opportunities else [],
                automation_potential=a.automation_potential,
                human_involvement=json.loads(a.human_involvement) if a.human_involvement else [],
                technologies=json.loads(a.technologies) if a.technologies else [],
                business_benefits=json.loads(a.business_benefits) if a.business_benefits else [],
                risks=json.loads(a.risks) if a.risks else [],
                reasoning=a.reasoning,
                confidence=a.confidence,
                created_at=a.created_at,
            ))
        return results

    def get_evidence(self, process_id: int) -> dict:
        from backend.models.research import EvidenceLink
        from backend.models.research import ResearchSource

        links = (
            self.db.query(EvidenceLink, ResearchSource)
            .join(ResearchSource, EvidenceLink.source_id == ResearchSource.id)
            .filter(EvidenceLink.process_id == process_id)
            .all()
        )

        evidence_items = []
        for link, source in links:
            evidence_items.append({
                "source_id": source.id,
                "title": source.title,
                "url": source.url,
                "publisher": source.publisher,
                "source_type": source.source_type,
                "excerpt": source.excerpt,
                "finding_summary": link.finding_summary,
                "relevance_score": link.relevance_score,
            })

        process = self.db.query(Process).filter(Process.id == process_id).first()
        return {
            "process_id": process_id,
            "process_name": process.name if process else "",
            "evidence": evidence_items,
            "total_sources": len(evidence_items),
        }


def settings_model():
    from backend.config import settings
    return settings.GEMINI_MODEL
