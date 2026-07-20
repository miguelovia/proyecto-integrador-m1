"""CLI interactivo para el sistema de soporte multi-departamento.

    python -m src.multi_agent_system
"""

import uuid

from src.agents.orchestrator import handle_query


def main() -> None:
    session_id = str(uuid.uuid4())
    print("Support router demo. Escribe 'exit' para salir.\n")

    while True:
        query = input("Ingresa tu pregunta: ").strip()
        if not query or query.lower() in {"exit", "quit", "salir"}:
            break

        result = handle_query(query, session_id=session_id)

        print(f"\n[{result.department} | confianza={result.confidence:.2f}]")
        print(result.answer)
        if result.sources:
            print(f"Fuentes: {', '.join(result.sources)}")
        if result.scores:
            s = result.scores
            print(
                f"(calidad — relevance {s.relevance}/5, "
                f"completeness {s.completeness}/5, accuracy {s.accuracy}/5)"
            )
        print()


if __name__ == "__main__":
    main()
