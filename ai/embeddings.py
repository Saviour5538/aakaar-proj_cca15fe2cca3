"""Embeddings — LOCAL (fastembed, no API key) by default, or an OpenAI-compatible API
(openai / azure / gemini via EMBEDDING_BASE_URL). Returns vectors of dimension 1536.
Select with EMBEDDING_PROVIDER (local|openai)."""
import os
from typing import List

EMBEDDING_DIM = 1536
_local = None


def _local_model():
    global _local
    if _local is None:
        from fastembed import TextEmbedding
        _local = TextEmbedding(model_name=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"), cache_dir=os.getenv("EMBEDDING_CACHE_DIR"))
    return _local


def embed_batch(texts: List[str]) -> List[List[float]]:
    items = list(texts)
    if not items:
        return []
    provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
    if provider == "local":
        return [list(map(float, v)) for v in _local_model().embed(items)]
    from openai import OpenAI
    client = OpenAI(base_url=os.getenv("EMBEDDING_BASE_URL") or None,
                    api_key=os.getenv("EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY"))
    resp = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"), input=items)
    return [list(map(float, d.embedding)) for d in resp.data]


def embed_text(text: str) -> List[float]:
    return embed_batch([text])[0]


def get_embedding(texts: List[str]) -> List[List[float]]:
    """Batch embed. Pass a LIST; to embed one string s use get_embedding([s])[0]."""
    return embed_batch(texts)
