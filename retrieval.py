"""
Milestone 4 — Embedding + vector store + retrieval for the F-1 Unofficial Guide.

Pipeline stages implemented here (see planning.md → Architecture):
    Embedding + Vector Store -> build_index()  embed 79 chunks, store in ChromaDB
    Retrieval                -> retrieve()      embed query, return top-k chunks

Retrieval approach (planning.md → Retrieval Approach):
  - Embedding model: all-MiniLM-L6-v2 (sentence-transformers), 384-dim, local/free.
  - Vector store: ChromaDB, persisted to ./chroma_db.
  - Distance: COSINE (0 = identical meaning, 2 = opposite). Good matches are < 0.5.
  - top-k: default 5 (tune after seeing real results).
  - Each chunk stored with metadata {source, chunk_index} for later attribution.

Run directly to (re)build the index and test retrieval on the 5 eval questions:
    python retrieval.py
"""

import os

import chromadb
from sentence_transformers import SentenceTransformer

from pipeline import build_corpus

EMBED_MODEL = "all-MiniLM-L6-v2"
CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
COLLECTION_NAME = "f1_guide"
DEFAULT_K = 5

# 5 evaluation questions from planning.md → Evaluation Plan, with the source doc
# each one should retrieve from (for the Milestone 4 retrieval sanity check).
EVAL_QUERIES = [
    ("Do I need an SSN or ITIN to open a US bank account as an F-1 student?", "banking"),
    ("How many hours can an F-1 student work on campus during summer vs. when classes are in session?", "employment"),
    ("Can F-1 students legally invest in stocks, and how are gains taxed?", "investing"),
    ("Why can't F-1 students use TurboTax, and what should they use instead?", "tax"),
    ("Does using pre-completion OPT reduce my post-completion OPT time?", "opt"),
]

# Cache the embedding model so we load the 87 MB model only once per process.
_embedder = None


def get_embedder():
    """Load (and cache) the all-MiniLM-L6-v2 sentence-transformer model."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def embed(texts):
    """Embed a list of strings into normalized 384-dim vectors (as plain lists)."""
    model = get_embedder()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()


def build_index(persist_path=CHROMA_PATH):
    """Embed every chunk from the pipeline and (re)load them into ChromaDB.

    Drops and recreates the collection each run so the index always matches the
    current chunks. Uses COSINE distance and stores {source, chunk_index} metadata.
    Returns the populated Chroma collection.
    """
    corpus = build_corpus()

    client = chromadb.PersistentClient(path=persist_path)
    # Start clean so re-running never leaves stale/duplicate vectors.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # cosine distance, range [0, 2]
    )

    collection.add(
        ids=[c["id"] for c in corpus],
        documents=[c["text"] for c in corpus],
        embeddings=embed([c["text"] for c in corpus]),
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in corpus],
    )
    return collection


def get_collection(persist_path=CHROMA_PATH):
    """Return the existing collection, building the index first if it's missing/empty."""
    client = chromadb.PersistentClient(path=persist_path)
    try:
        collection = client.get_collection(COLLECTION_NAME)
        if collection.count() > 0:
            return collection
    except Exception:
        pass
    return build_index(persist_path)


def retrieve(query, k=DEFAULT_K, collection=None):
    """Return the top-k most relevant chunks for a query.

    Each result: {"source", "chunk_index", "text", "distance"} (cosine distance,
    lower = more relevant), sorted nearest-first.
    """
    collection = collection or get_collection()
    result = collection.query(query_embeddings=embed([query]), n_results=k)
    hits = []
    for doc, meta, dist in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        hits.append({
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "text": doc,
            "distance": dist,
        })
    return hits


# --------------------------------------------------------------------------- #
# Retrieval test (Milestone 4 checkpoint)
# --------------------------------------------------------------------------- #
def _test_retrieval(k=DEFAULT_K):
    collection = build_index()
    print(f"Indexed {collection.count()} chunks into ChromaDB "
          f"({EMBED_MODEL}, cosine distance).\n")
    print("=" * 78)
    print(f"RETRIEVAL TEST — top-{k} chunks per query (distance: 0=identical, <0.5=good)")
    print("=" * 78)

    for query, expected_src in EVAL_QUERIES:
        hits = retrieve(query, k=k, collection=collection)
        top = hits[0]
        match = "OK" if expected_src in top["source"] else "MISS"
        print(f"\nQ: {query}")
        print(f"   expected source ~ {expected_src}  |  top hit: {top['source']} "
              f"(dist {top['distance']:.3f})  [{match}]")
        for i, h in enumerate(hits):
            preview = h["text"].replace("\n", " ")
            if len(preview) > 100:
                preview = preview[:100] + "..."
            print(f"   {i+1}. [{h['distance']:.3f}] {h['source']} c{h['chunk_index']}: {preview}")


if __name__ == "__main__":
    _test_retrieval()
