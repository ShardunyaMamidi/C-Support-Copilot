from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

from app.modules.rag.retriever import retrieve_chunks

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
  points = await retrieve_chunks(data.query, data.top_k, data.tags)

  return [
        SearchResponse(**p)
        for p in points
    ]

