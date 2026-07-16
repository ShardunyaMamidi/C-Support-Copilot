from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.agents.chains import build_rag_chain, build_triage_chain
from app.modules.agents.schemas import (
  AnswerRequest, AnswerResponse, TriageResponse
)
from app.modules.rag.retriever import retrieve_chunks
from app.modules.crud import service
from app.modules.crud.schemas import TicketUpdate
from app.modules.crud.models import TicketPriority

agent_router = APIRouter()

@agent_router.post("/answer", response_model=AnswerResponse)
async def answer_question(data: AnswerRequest):
  chain = build_rag_chain(provider=data.provider)
  answer = await chain.ainvoke({"question": data.question})
  chunks = await retrieve_chunks(data.question)

  return AnswerResponse(
    answer=answer,
    sources=chunks
  )

@agent_router.post("/triage/{ticket_id}", response_model=TriageResponse)
async def triage_ticket(ticket_id: uuid.UUID, provider: str = "gemini", db: AsyncSession = Depends(get_db)):
  ticket = await service.get_ticket(db, ticket_id)
  if ticket is None:
    raise HTTPException(status_code=404, detail="Ticket not found")

  chain = build_triage_chain(provider=provider)
  result = await chain.ainvoke({"subject": ticket.subject, "body": ticket.body})

  updated = await service.update_ticket(db, ticket, TicketUpdate(
    category=result.category,
    priority=TicketPriority(result.priority)
  ))

  return TriageResponse(ticket=updated, triage=result)
