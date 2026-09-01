# Research Methodology Documentation

## Overview

The research/evidence layer associates external sources with process analyses to support AI recommendations with traceable evidence.

## Research Sources

Pre-loaded sources include publications from:

| Publisher | Type | Coverage |
|-----------|------|----------|
| McKinsey & Company | Industry Report | AI in banking, automation value |
| Bank for International Settlements | Regulatory | AI adoption in financial services |
| Federal Reserve | Government | Fraud detection, credit risk |
| Deloitte | Industry Report | AI in lending, document processing |
| PwC | Industry Report | Customer onboarding, KYC |
| Basel Committee | Regulatory | AI risk management principles |
| IMF | Government | AML compliance, financial crime |
| Accenture | Industry Report | Treasury management, AI efficiency |
| Gartner | Industry Report | Document processing, IDP |
| Bain & Company | Industry Report | Customer service AI |
| FDIC | Government | Credit risk ML models |
| OCC | Regulatory | RegTech compliance |

## Evidence Linking Process

1. **Keyword Matching**: Process name/function words matched against source excerpts
2. **Domain Relevance**: Banking function keywords checked against source content
3. **Relevance Scoring**: Based on keyword overlap count
4. **Deduplication**: Same source not linked twice to same process

## Evidence Traceability

Every AI recommendation can be traced to:
- Specific research sources (title, URL, publisher)
- Finding summaries from those sources
- Relevance scores indicating evidence strength
- Analysis timestamp linking evidence to specific AI output

## Limitations

- Sources are pre-loaded; no real-time web search
- Matching is keyword-based, not semantic
- Evidence indicates support, not proof
- Missing evidence clearly marked as unavailable

## Never Fabricate

The system never generates fake citations. If no research source matches:
- Analysis proceeds without evidence links
- UI indicates "No external research available"
- User can manually review process analysis without evidence backing
