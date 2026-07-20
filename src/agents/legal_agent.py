"""RAG agent de Legal — grounded en data/legal_docs/*.md.

No se mencionó explícitamente en la separación hr/tech/finance, pero se
mantiene como su propio módulo (mismo patrón que los otros tres) para que el
departamento "legal" que el orchestrator ya clasifica siga teniendo un RAG
agent funcional detrás, en vez de lanzar un error al enrutar.
"""

from typing import Dict

from langchain_core.prompts import ChatPromptTemplate

from app.rag_common import build_department_chain, build_department_prompt

DEPARTMENT = "legal"

DEPARTMENT_BRIEFS: Dict[str, str] = {
    DEPARTMENT: (
        "Legal: contract and NDA review, data privacy/compliance (GDPR-style "
        "obligations), terms of service, IP and liability questions."
    )
}

_rag_chain = None


def _build_prompt(department: str = DEPARTMENT) -> ChatPromptTemplate:
    return build_department_prompt(department, DEPARTMENT_BRIEFS[department])


def get_rag_chain(department: str = DEPARTMENT):
    global _rag_chain
    if department != DEPARTMENT:
        raise ValueError(f"legal_agent only serves '{DEPARTMENT}', got '{department}'")
    if _rag_chain is None:
        _rag_chain = build_department_chain(department, DEPARTMENT_BRIEFS[department])
    return _rag_chain
