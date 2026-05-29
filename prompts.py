"""Prompt templates for BuildLens AI document generation.

Each entry in GENERATORS maps a human-friendly document name to an
instruction. The instruction is passed to the RAG chain so the answer is
grounded in the ESG knowledge base. Keep wording plain and practical.
"""

GENERATORS = {
    "Executive summary": (
        "Write a short executive summary for senior leaders covering the key "
        "ESG and sustainability points relevant to construction. Use clear, "
        "non-technical language and keep it under 250 words."
    ),
    "ESG gap analysis": (
        "Produce an ESG gap analysis for a construction project. Highlight "
        "common gaps across embodied carbon, circular economy, energy "
        "efficiency, climate resilience, social value and supply chain "
        "transparency, and suggest where to focus first."
    ),
    "Board briefing": (
        "Write a concise board briefing on ESG performance in construction. "
        "Explain why it matters, the main risks and opportunities, and three "
        "recommended actions. Avoid jargon."
    ),
    "Tender checklist": (
        "Create a practical ESG checklist a bid or tender manager can use to "
        "respond to sustainability questions in construction tenders. Use "
        "short, clear checklist items."
    ),
    "Action plan": (
        "Draft a step-by-step ESG improvement action plan for a construction "
        "company. Group actions by short term, medium term and long term."
    ),
    "LinkedIn post": (
        "Write a professional but approachable LinkedIn post about improving "
        "ESG and sustainability in construction. Keep it engaging and under "
        "150 words."
    ),
    "Client email": (
        "Write a polite, professional email to a client summarising the ESG "
        "considerations for their construction project and offering next steps."
    ),
    "Presentation outline": (
        "Create a slide-by-slide outline for a short presentation on ESG in "
        "construction. Give each slide a title and two or three bullet points."
    ),
}
