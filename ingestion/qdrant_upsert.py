import asyncio
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sqlalchemy import select

from app.config import settings
from app.database import SessionLocal
from app.modules.crud.models import KBArticle
from ingestion.chunking import chunk_article_body
from ingestion.embedding import load_cache, embed_document

COLLECTION_NAME = "kb_chunks"
VECTOR_SIZE = 768

client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key, timeout=60)

def ensure_collection() -> None:
  if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
      collection_name=COLLECTION_NAME,
      vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

async def sync_articles(batch_size: int = 50) -> int:
  ensure_collection()
  cache = load_cache()
  synced = 0

  async with SessionLocal() as session:
    result = await session.execute(
      select(KBArticle).where(KBArticle.qdrant_synced == False)
    )
    articles = result.scalars().all()

    for article in articles:
      # We are chunking and embedding only the article's body as it has both the question and answer
      chunks = chunk_article_body(article.body)
      points = []

      for chunk in chunks:
        embedding = embed_document(chunk, cache)
        points.append(
          PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
              "article_id": str(article.id),
              "title": article.title,
              "source_url": article.source_url,
              "tags": article.tags,
              "chunk_text": chunk,
            }
          )
        )
      client.upsert(collection_name=COLLECTION_NAME, points=points)
      article.qdrant_synced = True
      synced += 1

      if synced % batch_size == 0:
        await session.commit()
        print(f"synced {synced}/{len(articles)} articles", flush=True)

      await session.commit()
  print(f"done...synced {synced} articles total", flush=True)
  return synced

if __name__ == "__main__":
  asyncio.run(sync_articles())

