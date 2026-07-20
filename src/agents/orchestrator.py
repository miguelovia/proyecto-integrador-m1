from typing import Dict, List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.config import settings
from app.evaluator import evaluate_response
from app.observability import get_langchain_handler, get_trace_url, start_trace
from app.schemas import ClassificationResult, RoutingResult
from src.agents.finance_agent import DEPARTMENT_BRIEFS as FINANCE_BRIEFS
from src.agents.finance_agent import get_rag_chain as get_finance_chain
from src.agents.hr_agent import DEPARTMENT_BRIEFS as HR_BRIEFS
from src.agents.hr_agent import get_rag_chain as get_hr_chain
from src.agents.legal_agent import DEPARTMENT_BRIEFS as LEGAL_BRIEFS
from src.agents.legal_agent import get_rag_chain as get_legal_chain
from src.agents.tech_agent import DEPARTMENT_BRIEFS as TECH_BRIEFS
from src.agents.tech_agent import get_rag_chain as get_tech_chain

DEPARTMENT_BRIEFS: Dict[str, str] = {
    **HR_BRIEFS,
    **TECH_BRIEFS,
    **FINANCE_BRIEFS,
    **LEGAL_BRIEFS,
}

# Each entry is the get_rag_chain(department) callable exported by that
# department's own agent module — the orchestrator never builds a chain
# itself, it only decides which specialized agent should handle the ticket.
_RAG_CHAIN_GETTERS = {
    "hr": get_hr_chain,
    "it": get_tech_chain,
    "finance": get_finance_chain,
    "legal": get_legal_chain,
}

_CLASSIFIER_SYSTEM = """You are a routing classifier for a company's internal support desk.
Read the employee's question and decide which single department should handle it.

Departments:
- hr: {hr}
- it: {it}
- finance: {finance}
- legal: {legal}

Common misrouting traps to avoid:
- Payroll deduction or paycheck amount questions -> finance, not hr.
- Software license cost or purchase approval -> finance, not it.
- Employment contract or offer-letter wording -> legal, not hr.
- Data breach or customer-data handling -> legal, not it.
- VPN/account access problems -> it, even if the underlying reason is a contractor agreement (legal).

Pick exactly one department. If the question could plausibly fit more than one, choose whichever \
department owns the underlying policy or system, not the one merely mentioned in passing."""

_classifier_llm = None


def _get_classifier():
    global _classifier_llm
    if _classifier_llm is None:
        llm = ChatOpenAI(
            model=settings.orchestrator_model,
            temperature=0,
            api_key=settings.openai_api_key,
        )
        _classifier_llm = llm.with_structured_output(ClassificationResult)
    return _classifier_llm


def _build_classifier_prompt() -> ChatPromptTemplate:
    system = _CLASSIFIER_SYSTEM.format(**DEPARTMENT_BRIEFS)
    return ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{input}"),
        ]
    )


def classify(query: str, callbacks: Optional[list] = None) -> ClassificationResult:
    chain = _build_classifier_prompt() | _get_classifier()
    config = {"callbacks": callbacks} if callbacks else {}
    return chain.invoke({"input": query}, config=config)


def _extract_sources(context_docs: List) -> List[str]:
    seen: List[str] = []
    for doc in context_docs:
        name = doc.metadata.get("source", "unknown")
        if name not in seen:
            seen.append(name)
    return seen


def handle_query(
    query: str,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    run_evaluation: bool = True,
) -> RoutingResult:
    with start_trace(
        name="support-ticket",
        input_data={"query": query},
        session_id=session_id,
        user_id=user_id,
    ) as trace:
        handler = get_langchain_handler()

        classification = classify(query, callbacks=[handler])

        get_chain = _RAG_CHAIN_GETTERS.get(classification.department)
        if get_chain is None:
            raise ValueError(f"Unsupported department: {classification.department}")

        result = get_chain(classification.department).invoke(
            {"input": query}, config={"callbacks": [handler]}
        )
        answer = result["answer"]
        sources = _extract_sources(result["context"])

        trace.update(output={"department": classification.department, "answer": answer})

        scores = None
        if run_evaluation:
            scores = evaluate_response(
                trace=trace,
                query=query,
                department=classification.department,
                answer=answer,
                context_docs=result["context"],
            )

        return RoutingResult(
            query=query,
            department=classification.department,
            confidence=classification.confidence,
            reasoning=classification.reasoning,
            answer=answer,
            sources=sources,
            trace_id=trace.trace_id,
            trace_url=get_trace_url(trace.trace_id),
            scores=scores,
        )
