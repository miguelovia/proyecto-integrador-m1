from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.config import settings
from app.observability import get_langchain_handler
from app.schemas import EvaluationScores

_JUDGE_SYSTEM = """Eres un auditor de calidad para el asistente de IA de una mesa de soporte interna.
Se te mostrará la pregunta del empleado, la documentación interna que se recuperó para responderla \
y la respuesta del asistente.

Puntúa la respuesta en tres dimensiones, cada una de 1 (muy mala) a 5 (excelente):
- relevance: ¿responde directamente lo que realmente se preguntó?
- completeness: ¿cubre todo lo que la pregunta necesita, dado el contexto disponible?
- accuracy: ¿cada afirmación de la respuesta está respaldada por el contexto recuperado, sin nada inventado?

Sé estricto, especialmente con accuracy: una respuesta que suena segura pero no está fundamentada \
en el contexto proporcionado debe puntuar bajo, incluso si "suena correcta"."""

_judge_llm = None


def _get_judge():
    global _judge_llm
    if _judge_llm is None:
        llm = ChatOpenAI(
            model=settings.evaluator_model,
            temperature=0,
            api_key=settings.openai_api_key,
        )
        _judge_llm = llm.with_structured_output(EvaluationScores)
    return _judge_llm


def _build_judge_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", _JUDGE_SYSTEM),
            (
                "human",
                "Department: {department}\n\n"
                "Question:\n{query}\n\n"
                "Retrieved context:\n{context}\n\n"
                "Assistant answer:\n{answer}",
            ),
        ]
    )


def evaluate_response(
    trace,
    query: str,
    department: str,
    answer: str,
    context_docs: List,
) -> Optional[EvaluationScores]:
    """Score one answer on relevance/completeness/accuracy and push the scores
    back onto the same Langfuse trace, so low-quality responses are visible
    in Langfuse dashboards/alerts before they reach a customer — without
    blocking the ticket if the judge call itself fails.
    """
    context_text = "\n\n".join(doc.page_content for doc in context_docs) or (
        "(no context retrieved)"
    )

    chain = _build_judge_prompt() | _get_judge()

    try:
        handler = get_langchain_handler()
        scores = chain.invoke(
            {
                "department": department,
                "query": query,
                "context": context_text,
                "answer": answer,
            },
            config={"callbacks": [handler]},
        )
    except Exception as exc:  # noqa: BLE001 - evaluation must never break the ticket
        trace.create_event(name="evaluator_error", level="ERROR", status_message=str(exc))
        return None

    for dimension in ("relevance", "completeness", "accuracy"):
        trace.score_trace(
            name=f"eval_{dimension}",
            value=getattr(scores, dimension) / 5,
            comment=scores.rationale,
        )

    average = (scores.relevance + scores.completeness + scores.accuracy) / 3
    trace.score_trace(name="eval_overall", value=average / 5, comment=scores.rationale)

    return scores
