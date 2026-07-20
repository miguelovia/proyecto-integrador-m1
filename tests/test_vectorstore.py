import pytest

pytest.importorskip("langchain_chroma")
pytest.importorskip("sentence_transformers")

from app.config import settings  # noqa: E402
from app.vectorstore import DATA_DIR_BY_DEPARTMENT, build_vectorstore  # noqa: E402


def test_every_department_has_a_data_dir_mapping():
    for department in settings.departments:
        assert department in DATA_DIR_BY_DEPARTMENT, f"falta el mapeo de carpeta para {department}"


def test_knowledge_base_files_exist_for_every_department():
    for department in settings.departments:
        source_dir = settings.data_dir / DATA_DIR_BY_DEPARTMENT[department]
        assert source_dir.exists(), f"falta la carpeta de datos para {department}"
        assert list(source_dir.glob("*.md")), f"no hay documentos .md para {department}"


@pytest.mark.slow
def test_build_vectorstore_indexes_and_retrieves_relevant_chunks(tmp_path, monkeypatch):
    # Downloads the embedding model on first run and hits disk for the Chroma
    # collection — kept as a separate "slow" test so the fast suite stays fast.
    monkeypatch.setattr(settings, "chroma_persist_dir", tmp_path)

    store = build_vectorstore("hr")
    indexed_ids = store.get()["ids"]
    assert len(indexed_ids) > 0

    results = store.similarity_search("¿cuántos días de vacaciones tengo al año?", k=2)
    assert results
    assert any("pto_policy" in doc.metadata.get("source", "") for doc in results)
