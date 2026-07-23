"""
Simple RAG index over data/brand_sources.md.

Splits the approved brand talking points into small chunks, embeds them
locally (sentence-transformers, no external embeddings API), and persists
a FAISS vector store so agents can retrieve grounded context instead of
inventing claims about Coffra.
"""

from __future__ import annotations

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT_DIR = Path(__file__).resolve().parent.parent
BRAND_SOURCES_PATH = ROOT_DIR / "data" / "brand_sources.md"
INDEX_DIR = ROOT_DIR / "data" / "brand_sources_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_embeddings: HuggingFaceEmbeddings | None = None
_index: FAISS | None = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def build_index() -> FAISS:
    """Chunk data/brand_sources.md, embed it, and persist the FAISS index."""
    text = BRAND_SOURCES_PATH.read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=40,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = [c.strip() for c in splitter.split_text(text) if c.strip()]
    docs = [Document(page_content=chunk) for chunk in chunks]

    index = FAISS.from_documents(docs, _get_embeddings())
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index.save_local(str(INDEX_DIR))
    return index


def load_index() -> FAISS:
    """Load the persisted index, building it on first use."""
    global _index
    if _index is not None:
        return _index
    if not INDEX_DIR.exists():
        _index = build_index()
    else:
        _index = FAISS.load_local(
            str(INDEX_DIR), _get_embeddings(), allow_dangerous_deserialization=True
        )
    return _index


def get_relevant_chunks(query: str, k: int = 3) -> list[str]:
    """Return the top-k brand_sources.md chunks most relevant to query."""
    index = load_index()
    results = index.similarity_search(query, k=k)
    return [doc.page_content for doc in results]


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    build_index()
    for q in ["scor de calificare lead", "rezultate model XGBoost", "ce nu promitem"]:
        print(f"--- query: {q!r} ---")
        for chunk in get_relevant_chunks(q, k=2):
            print(chunk)
            print("...")
