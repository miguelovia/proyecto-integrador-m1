"""Corre un lote de tickets de ejemplo a través del orchestrator.

    python -m src.samples
"""

import json
from src.agents.orchestrator import handle_query


SAMPLE_TICKETS = [
    ("¿Cuántos días de vacaciones tengo al año y cómo los solicito?", "hr"),
    ("¿Donde se encuentra el portal de RH para solicitar días libres?", "hr"),
    ("¿Qué requieren los Roles 100% remotos?", "hr"),
    ("¿La instalación de software estándar requiere aprobación?", "finance"),
    ("Olvidé mi contraseña y no puedo entrar a la VPN, ¿qué hago?", "it"),
    ("¿Cuál es el límite de viáticos de comida por día en un viaje de trabajo?", "finance"),
    ("Necesito que legal revise un NDA antes de firmarlo con un proveedor", "legal"),
    ("Me descontaron de más en mi nómina este mes, ¿a quién le escribo?", "finance"),
    ("¿Necesito aprobación de compras para una licencia de software nueva?", "finance"),
    ("Sospecho que se filtraron datos de un cliente, ¿qué hago?", "legal"),
]


def main() -> None:
    for query, expected in SAMPLE_TICKETS:
        result = handle_query(query, session_id="demo-session")
        match = "OK" if result.department == expected else "REVISAR"

        """ print("=" * 88)
        print(f"Query: {result.query}")
        print(
            f"Departamento: {result.department}  (esperado: {expected}) [{match}]  "
            f"confianza={result.confidence:.2f}"
        )
        print(f"Motivo de ruteo: {result.reasoning}")
        print(f"Respuesta:\n{result.answer}")
        print(f"Fuentes: {', '.join(result.sources) or 'ninguna'}")

        if result.scores:
            s = result.scores
            print(
                f"Evaluación -> relevance={s.relevance}/5 "
                f"completeness={s.completeness}/5 accuracy={s.accuracy}/5"
            ) """
        
        json_result = {
        "user_question": query,
        "answer": result.answer,
        "department": result.department,
        "expected_department": expected,
        "match": match,
        "confidence": result.confidence,
        "reasoning": result.reasoning,
        "sources": result.sources,
        "scores": {
            "relevance": result.scores.relevance if result.scores else None,
            "completeness": result.scores.completeness if result.scores else None,
            "accuracy": result.scores.accuracy if result.scores else None,
            }
        }

        print(json.dumps(json_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
