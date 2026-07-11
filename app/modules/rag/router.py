from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

from app.modules.rag.embedder import embed_query
from app.modules.rag.retriever import search

rag_router = APIRouter()

class SearchRequest(BaseModel):
  query: str
  top_k: int = 5
  tags: Optional[list[str]] = None

class SearchResponse(BaseModel):
  title: str
  source_url: Optional[str] = None
  chunk_text: str
  score: float


@rag_router.post("/search")
async def search_query(data: SearchRequest):
  query_vector = await embed_query(data.query)
  points = await search(query_vector, top_k=data.top_k, tags=data.tags)

  return [
        SearchResponse(
            title=p.payload["title"],
            source_url=p.payload.get("source_url"),
            chunk_text=p.payload["chunk_text"],
            score=p.score,
        )
        for p in points
    ]

