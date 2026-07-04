from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from typing import Optional
from app.modules.crud.schemas import (
  TicketCreate,
  TicketRead,
  TicketUpdate,
  CustomerCreate,
  CustomerRead,
  CustomerUpdate,
  KBArticleCreate,
  KBArticleRead,
  KBArticleUpdate )
from app.modules.crud import service
from app.database import get_db
from app.modules.crud.models import TicketStatus
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

crud_router = APIRouter()

# Tickets endpoints

@crud_router.post("/tickets", response_model=TicketRead, status_code=http_status.HTTP_201_CREATED, tags=["tickets"])
async def create_ticket_endpoint(data: TicketCreate, db: AsyncSession = Depends(get_db)):
  return await service.create_ticket(db, data)

@crud_router.get("/tickets", response_model=list[TicketRead], tags=["tickets"])
async def list_tickets_endpoint(skip: int = 0, limit: int = 20, status: Optional[TicketStatus] = None, db: AsyncSession = Depends(get_db)):
  return await service.list_tickets(db, skip=skip, limit=limit, status=status)

@crud_router.get("/tickets/{ticket_id}", response_model=TicketRead, tags=["tickets"])
async def get_ticket_endpoint (ticket_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
  ticket = await service.get_ticket(db, ticket_id)
  if ticket is None:
    raise HTTPException(status_code=404, detail="Ticket not found")
  return ticket

@crud_router.patch("/tickets/{ticket_id}", response_model=TicketRead, tags=["tickets"])
async def patch_ticket_endpoint (ticket_id: uuid.UUID, data: TicketUpdate, db: AsyncSession = Depends(get_db)):
  ticket = await service.get_ticket(db, ticket_id)
  if ticket is None:
    raise HTTPException(status_code=404, detail="Ticket not found")
  return await service.update_ticket(db, ticket, data)

@crud_router.delete("/tickets/{ticket_id}", status_code=http_status.HTTP_204_NO_CONTENT, tags=["tickets"])
async def delete_ticket_endpoint (ticket_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
  ticket = await service.get_ticket(db, ticket_id)
  if ticket is None:
    raise HTTPException(status_code=404, detail="Ticket not found")
  await service.delete_ticket(db, ticket)

# Customer endpoints

@crud_router.post("/customers", response_model=CustomerRead, status_code=http_status.HTTP_201_CREATED, tags=["customers"])
async def create_customer_endpoint(data: CustomerCreate, db: AsyncSession = Depends(get_db)):
  return await service.create_customer(db, data)

@crud_router.get("/customers", response_model=list[CustomerRead], tags=["customers"])
async def list_customers_endpoint(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
  return await service.list_customers(db, skip=skip, limit=limit)

@crud_router.get("/customers/{customer_id}", response_model=CustomerRead, tags=["customers"])
async def get_customer_endpoint (customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
  customer = await service.get_customer(db, customer_id)
  if customer is None:
    raise HTTPException(status_code=404, detail="Customer not found")
  return customer

@crud_router.patch("/customers/{customer_id}", response_model=CustomerRead, tags=["customers"])
async def patch_customers_endpoint (customer_id: uuid.UUID, data: CustomerUpdate, db: AsyncSession = Depends(get_db)):
  customer = await service.get_customer(db, customer_id)
  if customer is None:
    raise HTTPException(status_code=404, detail="Customer not found")
  return await service.update_customer(db, customer, data)

@crud_router.delete("/customers/{customer_id}", status_code=http_status.HTTP_204_NO_CONTENT, tags=["customers"])
async def delete_customers_endpoint (customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
  customer = await service.get_customer(db, customer_id)
  if customer is None:
    raise HTTPException(status_code=404, detail="Customer not found")
  await service.delete_customer(db, customer)

# KBArticle Endpoints

@crud_router.post("/kb", response_model=KBArticleRead, status_code=http_status.HTTP_201_CREATED, tags=["kb"])
async def create_kb_article_endpoint(data: KBArticleCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_kb_article(db, data)

@crud_router.get("/kb", response_model=list[KBArticleRead], tags=["kb"])
async def list_kb_articles_endpoint(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    return await service.list_kb_articles(db, skip=skip, limit=limit)

@crud_router.get("/kb/{article_id}", response_model=KBArticleRead, tags=["kb"])
async def get_kb_article_endpoint(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    article = await service.get_kb_article(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="KB article not found")
    return article

@crud_router.patch("/kb/{article_id}", response_model=KBArticleRead, tags=["kb"])
async def patch_kb_article_endpoint(article_id: uuid.UUID, data: KBArticleUpdate, db: AsyncSession = Depends(get_db)):
    article = await service.get_kb_article(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="KB article not found")
    return await service.update_kb_article(db, article, data)

@crud_router.delete("/kb/{article_id}", status_code=http_status.HTTP_204_NO_CONTENT, tags=["kb"])
async def delete_kb_article_endpoint(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    article = await service.get_kb_article(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="KB article not found")
    await service.delete_kb_article(db, article)