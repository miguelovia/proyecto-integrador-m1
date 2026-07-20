"""RAG agent de soporte IT/Tech — grounded en data/tech_docs/*.md.

El módulo se llama tech_agent, pero conserva la clave de departamento "it"
para alinearse con la lista DEPARTMENTS de app/config.py y el Literal
Department de app/schemas.py; app/vectorstore.py::DATA_DIR_BY_DEPARTMENT
mapea "it" -> data/tech_docs/.
"""

from typing import Dict

from langchain_core.prompts import ChatPromptTemplate

from app.rag_common import build_department_chain, build_department_prompt

DEPARTMENT = "it"

DEPARTMENT_BRIEFS: Dict[str, str] = {
    DEPARTMENT: (
        "IT Support: passwords and MFA, VPN and remote access, hardware "
        "requests, software installs, account access issues."
    )
}

_rag_chain = None


def _build_prompt(department: str = DEPARTMENT) -> ChatPromptTemplate:
    return build_department_prompt(department, DEPARTMENT_BRIEFS[department])


def get_rag_chain(department: str = DEPARTMENT):
    global _rag_chain
    if department != DEPARTMENT:
        raise ValueError(f"tech_agent only serves '{DEPARTMENT}', got '{department}'")
    if _rag_chain is None:
        _rag_chain = build_department_chain(department, DEPARTMENT_BRIEFS[department])
    return _rag_chain
