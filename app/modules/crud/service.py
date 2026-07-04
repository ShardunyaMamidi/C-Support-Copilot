import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.crud.models import Ticket, TicketStatus, Customer, KBArticle
from app.modules.crud.schemas import (
  TicketCreate,
  TicketUpdate,
  CustomerCreate,
  CustomerUpdate,
  KBArticleCreate,
  KBArticleUpdate)

# Tickets BL

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

# Customer BL

async def create_customer(db: AsyncSession, data: CustomerCreate):
  customer = Customer(**data.model_dump())
  db.add(customer)
  await db.commit()
  await db.refresh(customer)
  return customer

async def get_customer(db: AsyncSession, customer_id: uuid.UUID) -> Optional[Customer]:
  result = await db.execute(select(Customer).where(Customer.id == customer_id))
  return result.scalar_one_or_none()

async def list_customers(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[Customer]:
  query = select(Customer).offset(skip).limit(limit)
  result = await db.execute(query)
  return list(result.scalars().all())

async def update_customer(db: AsyncSession, customer: Customer, data: CustomerUpdate) -> Customer:
  for field, value in data.model_dump(exclude_unset=True).items():
    setattr(customer, field, value)
  await db.commit()
  await db.refresh(customer)
  return customer

async def delete_customer(db: AsyncSession, customer: Customer) -> None:
  await db.delete(customer)
  await db.commit()

# Knowledge Base BL

async def create_kb_article(db: AsyncSession, data: KBArticleCreate) -> KBArticle:
  kb_article = KBArticle(**data.model_dump())
  db.add(kb_article)
  await db.commit()
  await db.refresh(kb_article)
  return kb_article

async def get_kb_article(db: AsyncSession, article_id: uuid.UUID) -> Optional[KBArticle]:
  result = await db.execute(select(KBArticle).where(KBArticle.id == article_id))
  return result.scalar_one_or_none()

async def list_kb_articles(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[KBArticle]:
  query = select(KBArticle).offset(skip).limit(limit)
  result = await db.execute(query)
  return list(result.scalars().all())

async def update_kb_article(db: AsyncSession, kb_article: KBArticle, data: KBArticleUpdate) -> KBArticle:
  for field, value in data.model_dump(exclude_unset=True).items():
    setattr(kb_article, field, value)
  await db.commit()
  await db.refresh(kb_article)
  return kb_article

async def delete_kb_article(db: AsyncSession, kb_article: KBArticle) -> None:
  await db.delete(kb_article)
  await db.commit()