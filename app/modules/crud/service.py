import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.crud.models import Ticket, TicketStatus
from app.modules.crud.schemas import TicketCreate, TicketUpdate

async def create_ticket(db: AsyncSession, data: TicketCreate) -> Ticket:
  ticket = Ticket(**data.model_dump())
  db.add(ticket)
  await db.commit()
  await db.refresh(ticket)
  return ticket

async def get_ticket(db: AsyncSession, ticket_id: uuid.UUID) -> Optional[Ticket]:
  result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
  return result.scalar_one_or_none()

async def list_tickets(db: AsyncSession, skip: int = 0, limit: int = 20, status: Optional[TicketStatus] = None) -> list[Ticket]:
  query = select(Ticket)
  if status is not None:
    query = query.where(Ticket.status == status)
  query = query.offset(skip).limit(limit=limit)
  result = await db.execute(query)
  return list(result.scalars().all())

async def update_ticket(db: AsyncSession, ticket: Ticket, data: TicketUpdate) -> Ticket:
  for field, value in data.model_dump(exclude_unset=True).items():
    # ticket.field = value
    setattr(ticket, field, value)
  await db.commit()
  await db.refresh(ticket)
  return ticket

async def delete_ticket(db: AsyncSession, ticket: Ticket) -> None:
  await db.delete(ticket)
  await db.commit()