import shutil
from pathlib import Path
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings

DATA_DIR_BY_DEPARTMENT = {
    "hr": "hr_docs",
    "it": "tech_docs",
    "finance": "finance_docs",
    "legal": "legal_docs",
}

_embeddings: Optional[HuggingFaceEmbeddings] = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """Obtiene los embebdings
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model_name)
    return _embeddings


def _collection_dir(department: str) -> Path:
    return settings.chroma_persist_dir / department


def _data_dir_name(department: str) -> str:
    try:
        return DATA_DIR_BY_DEPARTMENT[department]
    except KeyError:
        raise ValueError(f"Unknown department: {department}") from None


def _load_documents(department: str) -> List:
    source_dir = settings.data_dir / _data_dir_name(department)
    if not source_dir.exists():
        raise FileNotFoundError(
            f"No knowledge base found for department '{department}' at {source_dir}"
        )

    documents = []
    for path in sorted(source_dir.glob("*.md")):
        loaded = TextLoader(str(path), encoding="utf-8").load()
        for doc in loaded:
            doc.metadata["source"] = path.name
            doc.metadata["department"] = department
        documents.extend(loaded)
    return documents


def build_vectorstore(department: str) -> Chroma:
    """(Re)build the persisted Chroma collection for one department from its
    markdown knowledge base in data/<DATA_DIR_BY_DEPARTMENT[department]>/.
    """
    documents = _load_documents(department)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(documents)

    persist_dir = _collection_dir(department)
    if persist_dir.exists():
        shutil.rmtree(persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)

    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=f"{department}_docs",
        persist_directory=str(persist_dir),
    )


def load_vectorstore(department: str) -> Chroma:
    """Load the persisted collection, building it on first use if it's empty."""
    persist_dir = _collection_dir(department)
    store = Chroma(
        collection_name=f"{department}_docs",
        embedding_function=get_embeddings(),
        persist_directory=str(persist_dir),
    )
    if not store.get()["ids"]:
        store = build_vectorstore(department)
    return store


def get_retriever(department: str, k: int = 4):
    store = load_vectorstore(department)
    return store.as_retriever(search_kwargs={"k": k})
