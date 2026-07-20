"""Construye (o reconstruye) el vector store de Chroma para cada departamento configurado.

Se corre una vez antes de la primera consulta, y de nuevo cada vez que cambie
la base de conocimiento en markdown bajo data/<departamento>_docs/:

    python -m src.vectorization
"""

from app.config import settings
from app.vectorstore import build_vectorstore


def main() -> None:
    for department in settings.departments:
        store = build_vectorstore(department)
        count = len(store.get()["ids"])
        print(f"[{department}] indexed {count} chunks")


if __name__ == "__main__":
    main()
