import asyncio
from sqlalchemy import select

from app.database import SessionLocal
from app.modules.crud.models import KBArticle
from ingestion.chunking import chunk_article_body
from ingestion.embedding import load_cache, embed_document

async def main():
  async with SessionLocal() as session:
    result = await session.execute(select(KBArticle).limit(1))
    article = result.scalar_one()

  chunks = chunk_article_body(article.body)
  print(f"article split into {len(chunks)} chunks")
  print(f"first chunk ({len(chunks[0])} chars):\n{chunks[0][:200]}...")

  cache = load_cache()
  embedding = embed_document(chunks[0], cache)
  print(f"embedding length: {len(embedding)}")
  print(f"first 5 values: {embedding[:5]}")

asyncio.run(main())