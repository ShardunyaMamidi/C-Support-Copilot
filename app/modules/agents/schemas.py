from typing import Literal
from pydantic import BaseModel

from app.modules.rag.router import SearchResponse
from app.modules.crud.schemas import TicketRead

class TriageResult(BaseModel):
  category: Literal[
    "pointers", "memory", "toolchain", "peripherals", "concurrency", "build", "other"
  ]

  priority: Literal["low", "medium", "high"]
  sentiment: Literal["neutral", "frustrated", "urgent"]
  summary: str

class AnswerRequest(BaseModel):
  question: str
  provider: str = "gemini"

class AnswerResponse(BaseModel):
  answer: str
  sources: list[SearchResponse]

class TriageResponse(BaseModel):
  ticket: TicketRead
  triage: TriageResult 