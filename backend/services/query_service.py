import json
import logging
from sqlalchemy.orm import Session
from backend.models.process import Process
from backend.models.analysis import ProcessAnalysis
from backend.models.score import ProcessScore
from backend.models.research import EvidenceLink
from backend.models.research import ResearchSource
from backend.schemas.query import QueryResponse, ProcessSummary
from backend.ai.llm_client import call_llm
from backend.ai.prompts import QUERY_SYSTEM_PROMPT
from backend.services.research_service import ResearchService
import asyncio

logger = logging.getLogger(__name__)


class QueryService:
    def __init__(self, db: Session):
        self.db = db

    def process_query(self, question: str) -> QueryResponse:
        lower_q = question.lower()

        if "human" in lower_q and ("led" in lower_q or "remain" in lower_q):
            return self._human_led_query()
        elif "top" in lower_q and ("opportunity" in lower_q or "potential" in lower_q or "automate" in lower_q):
            return self._top_opportunities_query()
        elif "risk" in lower_q:
            return self._risk_query()
        elif "research" in lower_q or "evidence" in lower_q or "source" in lower_q:
            return self._research_query(question)
        elif "why" in lower_q and ("score" in lower_q or "rank" in lower_q):
            return self._why_score_query(question)
        else:
            return self._general_query(question)

    def _human_led_query(self) -> QueryResponse:
        from backend.services.process_service import ProcessService
        svc = ProcessService(self.db)
        human_led = svc.get_human_led_processes()

        procs = [
            ProcessSummary(
                id=p["process_id"],
                name=p["process_name"],
                business_function=p["business_function"],
                automation_potential=p["automation_potential"],
            )
            for p in human_led[:10]
        ]

        reasons_text = "; ".join(
            [f"{p['process_name']}: {'; '.join(p['reasons'])}" for p in human_led[:5]]
        )

        answer = f"Based on analysis, {len(human_led)} processes should remain predominantly human-led due to high regulatory sensitivity, decision risk, or low automation feasibility. "
        if reasons_text:
            answer += f"Key examples: {reasons_text}"

        return QueryResponse(answer=answer, processes=procs)

    def _top_opportunities_query(self) -> QueryResponse:
        from backend.services.process_service import ProcessService
        svc = ProcessService(self.db)
        top = svc.get_top_processes(limit=10)

        procs = [
            ProcessSummary(
                id=p["process_id"],
                name=p["process_name"],
                business_function=p["business_function"],
                ai_score=p["total_score"],
                priority=p["priority"],
                automation_potential=p["automation_potential"],
            )
            for p in top
        ]

        answer = f"Top {len(top)} processes with highest AI potential:\n"
        for p in top:
            answer += f"#{p['rank']} {p['process_name']} (Score: {p['total_score']}, Priority: {p['priority']})\n"

        return QueryResponse(answer=answer, processes=procs)

    def _risk_query(self) -> QueryResponse:
        risky = (
            self.db.query(Process, ProcessScore, ProcessAnalysis)
            .join(ProcessAnalysis, Process.id == ProcessAnalysis.process_id)
            .join(ProcessScore, ProcessAnalysis.id == ProcessScore.analysis_id)
            .order_by(ProcessScore.risk_factor.desc())
            .limit(5)
            .all()
        )

        procs = [
            ProcessSummary(
                id=p.id,
                name=p.name,
                business_function=p.business_function,
                ai_score=round(s.total_score, 1),
                priority=s.priority,
            )
            for p, s, _ in risky
        ]

        answer = "Highest AI risk processes:\n"
        for p, s, a in risky:
            risks = json.loads(a.risks) if a.risks else []
            answer += f"- {p.name} (Risk: {s.risk_factor}/10): {'; '.join(risks[:2]) if risks else 'High inherent risk'}\n"

        return QueryResponse(answer=answer, processes=procs)

    def _research_query(self, question: str) -> QueryResponse:
        import re
        proc_match = re.search(r'process\s*(\d+)', question.lower())
        if proc_match:
            proc_id = int(proc_match.group(1))
            proc = self.db.query(Process).filter(Process.id == proc_id).first()
            if proc:
                analysis_svc_obj = __import__('backend.services.analysis_service', fromlist=['AnalysisService'])
                evidence = analysis_svc_obj.AnalysisService(self.db).get_evidence(proc_id)
                sources = evidence.get("evidence", [])
                answer = f"Research evidence for Process {proc_id} ({proc.name}):\n"
                if sources:
                    for s in sources:
                        answer += f"- [{s['source_type']}] {s['title']} ({s['publisher']}): {s['finding_summary'][:150]}...\n"
                else:
                    answer += "No external research sources currently linked. Research may be unavailable."

                return QueryResponse(
                    answer=answer,
                    processes=[ProcessSummary(id=proc.id, name=proc.name, business_function=proc.business_function)],
                    evidence=[s.get("title", "") for s in sources],
                )

        return self._general_query(question)

    def _why_score_query(self, question: str) -> QueryResponse:
        import re
        proc_match = re.search(r'process\s*(\d+)', question.lower())
        if proc_match:
            proc_id = int(proc_match.group(1))
            proc = self.db.query(Process).filter(Process.id == proc_id).first()
            analysis = self.db.query(ProcessAnalysis).filter(ProcessAnalysis.process_id == proc_id).first()
            score = (
                self.db.query(ProcessScore)
                .join(ProcessAnalysis, ProcessAnalysis.id == ProcessScore.analysis_id)
                .filter(ProcessAnalysis.process_id == proc_id)
                .first()
            )
            if proc and score:
                answer = f"Why Process {proc_id} ({proc.name}) has score {score.total_score}:\n"
                answer += f"Automation Potential: {score.automation_potential}/10\n"
                answer += f"Business Benefit: {score.business_benefit}/10\n"
                answer += f"Data Availability: {score.data_availability}/10\n"
                answer += f"AI Feasibility: {score.ai_feasibility}/10\n"
                answer += f"Process Repetition: {score.process_repetition}/10\n"
                answer += f"Risk Factor: {score.risk_factor}/10 (negative)\n"
                answer += f"Regulatory Sensitivity: {score.regulatory_sensitivity}/10 (negative)\n"
                if analysis:
                    answer += f"\nAI Reasoning: {analysis.reasoning[:300]}..."

                return QueryResponse(
                    answer=answer,
                    processes=[ProcessSummary(id=proc.id, name=proc.name, business_function=proc.business_function, ai_score=score.total_score, priority=score.priority)],
                )

        return self._general_query(question)

    def _general_query(self, question: str) -> QueryResponse:
        all_procs = (
            self.db.query(Process, ProcessScore, ProcessAnalysis)
            .join(ProcessAnalysis, Process.id == ProcessAnalysis.process_id, isouter=True)
            .join(ProcessScore, ProcessAnalysis.id == ProcessScore.analysis_id, isouter=True)
            .all()
        )

        context_lines = []
        for p, s, a in all_procs[:30]:
            score_val = round(s.total_score, 1) if s else "N/A"
            priority_val = s.priority if s else "N/A"
            context_lines.append(f"Process {p.id}: {p.name} | Function: {p.business_function} | Score: {score_val} | Priority: {priority_val}")

        context = "\n".join(context_lines)

        try:
            user_msg = f"Question: {question}\n\nProcess data:\n{context}"
            loop = asyncio.new_event_loop()
            raw = loop.run_until_complete(call_llm(QUERY_SYSTEM_PROMPT, user_msg))
            if "error" in raw:
                answer = f"Based on {len(all_procs)} analyzed processes: {question}\n\nTop processes by score:\n"
                for p, s, _ in all_procs[:5]:
                    if s:
                        answer += f"- {p.name} (Score: {s.total_score}, Priority: {s.priority})\n"
            else:
                answer = raw.get("choices", [{}])[0].get("message", {}).get("content", "") if isinstance(raw, dict) and "choices" in raw else str(raw)
        except Exception as e:
            logger.error(f"LLM query failed: {e}")
            answer = f"Based on {len(all_procs)} analyzed processes in the database. Please refer to the dashboard for detailed views."

        top_procs = [
            ProcessSummary(
                id=p.id,
                name=p.name,
                business_function=p.business_function,
                ai_score=round(s.total_score, 1) if s else None,
                priority=s.priority if s else None,
            )
            for p, s, _ in all_procs[:5]
        ]

        return QueryResponse(answer=answer, processes=top_procs)
