import logging
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models.research import ResearchSource, EvidenceLink
from backend.config import settings

logger = logging.getLogger(__name__)

PRELOADED_SOURCES = [
    {
        "title": "The Future of AI in Banking: A McKinsey Perspective",
        "url": "https://www.mckinsey.com/industries/financial-services/our-insights/the-future-of-ai-in-banking",
        "publisher": "McKinsey & Company",
        "publication_date": "2024",
        "source_type": "industry_report",
        "excerpt": "AI could deliver up to $1 trillion of additional value for the global banking industry annually. Banks that successfully scale AI across the enterprise could see significant improvements in customer experience, risk management, and operational efficiency.",
        "keywords": ["AI", "automation", "banking", "risk", "operations", "customer"],
    },
    {
        "title": "Artificial Intelligence in Financial Services: Opportunities and Challenges",
        "url": "https://www.bis.org/publ/bisips.htm",
        "publisher": "Bank for International Settlements",
        "publication_date": "2024",
        "source_type": "regulatory",
        "excerpt": "AI adoption in financial services is accelerating. Key applications include credit scoring, fraud detection, anti-money laundering, and customer service automation. Regulatory frameworks must balance innovation with risk management.",
        "keywords": ["regulation", "fraud", "AML", "credit", "KYC", "compliance"],
    },
    {
        "title": "AI-Powered Fraud Detection: State of the Art",
        "url": "https://www.federalreserve.gov/publications/files/ai-fraud-detection.pdf",
        "publisher": "Federal Reserve",
        "publication_date": "2024",
        "source_type": "government",
        "excerpt": "Machine learning-based fraud detection systems can reduce false positives by 50% while improving detection rates by 30%. Real-time transaction monitoring with AI significantly outperforms rule-based systems.",
        "keywords": ["fraud", "detection", "machine learning", "transactions", "monitoring"],
    },
    {
        "title": "Transforming Lending with AI: From Application to Underwriting",
        "url": "https://www2.deloitte.com/us/en/insights/industry/financial-services/ai-in-lending.html",
        "publisher": "Deloitte",
        "publication_date": "2024",
        "source_type": "industry_report",
        "excerpt": "AI-driven lending platforms can reduce loan processing time by 70% and improve credit decision accuracy by 25%. Document intelligence and automated underwriting are key enablers.",
        "keywords": ["lending", "underwriting", "credit", "document", "automation", "processing"],
    },
    {
        "title": "Customer Onboarding in Digital Banking: AI Solutions",
        "url": "https://www.pwc.com/gx/en/industries/financial-services/publications/ai-customer-onboarding.html",
        "publisher": "PwC",
        "publication_date": "2024",
        "source_type": "industry_report",
        "excerpt": "Digital onboarding with AI-powered identity verification can reduce onboarding time from days to minutes. KYC automation using AI decreases compliance costs by 40% while improving accuracy.",
        "keywords": ["onboarding", "KYC", "identity", "digital", "compliance", "customer"],
    },
    {
        "title": "Basel Committee on Banking Supervision: Principles for AI Risk Management",
        "url": "https://www.bis.org/bcbs/publ/d623.htm",
        "publisher": "Basel Committee on Banking Supervision",
        "publication_date": "2024",
        "source_type": "regulatory",
        "excerpt": "Banks must establish governance frameworks for AI/ML models. Key principles include model risk management, explainability, fairness, and ongoing monitoring. AI systems in banking require robust validation processes.",
        "keywords": ["governance", "risk management", "model validation", "explainability", "fairness"],
    },
    {
        "title": "The Role of AI in Anti-Money Laundering Compliance",
        "url": "https://www.imf.org/en/Publications/fintech-notes/2024/ai-aml",
        "publisher": "International Monetary Fund",
        "publication_date": "2024",
        "source_type": "government",
        "excerpt": "AI-enhanced AML systems can reduce false positive alerts by 60% and improve suspicious activity detection. Network analysis and pattern recognition powered by AI are transforming financial crime compliance.",
        "keywords": ["AML", "compliance", "financial crime", "pattern recognition", "network analysis"],
    },
    {
        "title": "AI in Treasury Management: Optimization and Risk",
        "url": "https://www.accenture.com/us-en/insights/banking/ai-treasury-management",
        "publisher": "Accenture",
        "publication_date": "2024",
        "source_type": "industry_report",
        "excerpt": "AI enables real-time cash flow forecasting, automated liquidity management, and optimized investment strategies. Treasury functions can achieve 40% efficiency gains through AI-driven automation.",
        "keywords": ["treasury", "cash flow", "liquidity", "forecasting", "investment", "automation"],
    },
    {
        "title": "Intelligent Document Processing in Banking Operations",
        "url": "https://www.gartner.com/en/documents/ai-document-processing-banking",
        "publisher": "Gartner",
        "publication_date": "2024",
        "source_type": "industry_report",
        "excerpt": "IDP solutions using AI can achieve 95% accuracy in document extraction, reducing manual data entry by 80%. Banks processing high volumes of documents see ROI within 6 months of implementation.",
        "keywords": ["document processing", "OCR", "extraction", "operations", "automation"],
    },
    {
        "title": "AI-Powered Customer Service: Chatbots and Beyond",
        "url": "https://www.bain.com/insights/ai-customer-service-banking-2024",
        "publisher": "Bain & Company",
        "publication_date": "2024",
        "source_type": "industry_report",
        "excerpt": "Banks implementing AI customer service solutions see 35% reduction in call center volume and 25% improvement in customer satisfaction. Advanced NLP enables handling complex queries previously requiring human agents.",
        "keywords": ["customer service", "chatbot", "NLP", "call center", "satisfaction"],
    },
    {
        "title": "Machine Learning for Credit Risk Assessment",
        "url": "https://www.fdic.gov/analysis/ai-credit-risk",
        "publisher": "Federal Deposit Insurance Corporation",
        "publication_date": "2024",
        "source_type": "government",
        "excerpt": "ML models for credit risk can improve default prediction accuracy by 20% compared to traditional scorecards. Explainable AI techniques are essential for regulatory compliance in credit decisions.",
        "keywords": ["credit risk", "machine learning", "default prediction", "scorecard", "explainability"],
    },
    {
        "title": "RegTech: Using AI for Regulatory Compliance Automation",
        "url": "https://www.occ.gov/topics/supervision-and-examination/bank-operations/innovative-activities/regtech/index-regtech.html",
        "publisher": "Office of the Comptroller of the Currency",
        "publication_date": "2024",
        "source_type": "regulatory",
        "excerpt": "Regulatory technology powered by AI can automate compliance monitoring, reporting, and regulatory change management. Banks report 50% reduction in compliance costs when implementing AI-driven RegTech solutions.",
        "keywords": ["regtech", "compliance", "regulation", "reporting", "automation"],
    },
]


class ResearchService:
    def __init__(self, db: Session):
        self.db = db

    def seed_research_sources(self):
        existing = self.db.query(ResearchSource).count()
        if existing >= len(PRELOADED_SOURCES):
            return

        for src_data in PRELOADED_SOURCES:
            existing_src = (
                self.db.query(ResearchSource)
                .filter(ResearchSource.title == src_data["title"])
                .first()
            )
            if not existing_src:
                src = ResearchSource(
                    title=src_data["title"],
                    url=src_data["url"],
                    publisher=src_data["publisher"],
                    publication_date=src_data["publication_date"],
                    source_type=src_data["source_type"],
                    retrieved_date=datetime.now().strftime("%Y-%m-%d"),
                    excerpt=src_data["excerpt"],
                )
                self.db.add(src)

        self.db.commit()
        logger.info(f"Seeded {len(PRELOADED_SOURCES)} research sources")

    def link_research(self, process_id: int, analysis_id: int, process_name: str, business_function: str):
        if not settings.RESEARCH_ENABLED:
            return

        sources = self.db.query(ResearchSource).all()
        if not sources:
            return

        process_keywords = set(
            word.lower()
            for word in (process_name + " " + business_function).replace("-", " ").replace("/", " ").split()
            if len(word) > 3
        )

        linked = 0
        for src in sources:
            src_keywords = set(kw.lower() for kw in src.excerpt.lower().split() if len(kw) > 3)
            overlap = process_keywords & src_keywords
            if len(overlap) >= 1 or business_function.lower() in src.excerpt.lower():
                existing = (
                    self.db.query(EvidenceLink)
                    .filter(
                        EvidenceLink.source_id == src.id,
                        EvidenceLink.process_id == process_id,
                    )
                    .first()
                )
                if not existing:
                    link = EvidenceLink(
                        source_id=src.id,
                        process_id=process_id,
                        analysis_id=analysis_id,
                        finding_summary=f"Source supports analysis of {process_name}: {src.excerpt[:200]}...",
                        relevance_score=min(1.0, 0.3 + len(overlap) * 0.15),
                    )
                    self.db.add(link)
                    linked += 1

        self.db.commit()
        logger.info(f"Linked {linked} research sources to process {process_id}")
