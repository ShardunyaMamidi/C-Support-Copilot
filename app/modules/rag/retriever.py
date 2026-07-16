from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny

from app.config import settings
from app.modules.rag.embedder import embed_query

COLLECTION_NAME = "kb_chunks"

client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key, timeout=60)


async def search(query_vector: list[float], top_k: int = 5, tags: list[str] | None = None):
  query_filter = None
  if tags:
    query_filter = Filter(
      must=[FieldCondition(key="tags", match=MatchAny(any=tags))]
    )

  result = await client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    query_filter=query_filter,
    limit=top_k,
    with_payload=True
  )

  return result.points

async def retrieve_chunks(query: str, top_k: int = 5, tags: list[str] | None = None) -> list[dict]:
  query_vector = await embed_query(query)
  points = await search(query_vector, top_k=top_k, tags=tags)

  return [
    {
      "title": p.payload["title"],
      "source_url": p.payload.get("source_url"),
      "chunk_text": p.payload["chunk_text"],
      "score": p.score,
    }
    for p in points
  ]