from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny

from app.config import settings

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