"""RAG agent de HR — grounded en data/hr_docs/*.md."""

from typing import Dict

from langchain_core.prompts import ChatPromptTemplate

from app.rag_common import build_department_chain, build_department_prompt

DEPARTMENT = "hr"

DEPARTMENT_BRIEFS: Dict[str, str] = {
    DEPARTMENT: (
        "Human Resources: onboarding, benefits, PTO/vacation and sick leave, "
        "parental leave, remote/hybrid work policy, workplace conduct."
    )
}

_rag_chain = None


def _build_prompt(department: str = DEPARTMENT) -> ChatPromptTemplate:
    return build_department_prompt(department, DEPARTMENT_BRIEFS[department])


def get_rag_chain(department: str = DEPARTMENT):
    global _rag_chain
    if department != DEPARTMENT:
        raise ValueError(f"hr_agent only serves '{DEPARTMENT}', got '{department}'")
    if _rag_chain is None:
        _rag_chain = build_department_chain(department, DEPARTMENT_BRIEFS[department])
    return _rag_chain
