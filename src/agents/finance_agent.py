"""RAG agent de Finance — grounded en data/finance_docs/*.md."""

from typing import Dict

from langchain_core.prompts import ChatPromptTemplate

from app.rag_common import build_department_chain, build_department_prompt

DEPARTMENT = "finance"

DEPARTMENT_BRIEFS: Dict[str, str] = {
    DEPARTMENT: (
        "Finance: expense reimbursement, invoicing, payroll timing and "
        "deductions, travel budget and per diem, purchase/software approvals."
    )
}

_rag_chain = None


def _build_prompt(department: str = DEPARTMENT) -> ChatPromptTemplate:
    return build_department_prompt(department, DEPARTMENT_BRIEFS[department])


def get_rag_chain(department: str = DEPARTMENT):
    global _rag_chain
    if department != DEPARTMENT:
        raise ValueError(f"finance_agent only serves '{DEPARTMENT}', got '{department}'")
    if _rag_chain is None:
        _rag_chain = build_department_chain(department, DEPARTMENT_BRIEFS[department])
    return _rag_chain
