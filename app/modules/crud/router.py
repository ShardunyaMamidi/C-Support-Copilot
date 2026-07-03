from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from typing import Optional
from app.modules.crud.schemas import TicketCreate, TicketRead, TicketUpdate
from app.modules.crud import service
from app.database import get_db
from app.modules.crud.models import TicketStatus
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

router = APIRouter()

@router.post("/tickets", response_model=TicketRead, status_code=http_status.HTTP_201_CREATED, tags=["tickets"])
async def create_ticket_endpoint(data: TicketCreate, db: AsyncSession = Depends(get_db)):
  return await service.create_ticket(db, data)

@router.get("/tickets", response_model=list[TicketRead], tags=["tickets"])
async def list_tickets_endpoint(skip: int = 0, limit: int = 20, status: Optional[TicketStatus] = None, db: AsyncSession = Depends(get_db)):
  return await service.list_tickets(db, skip=skip, limit=limit, status=status)

@router.get("/tickets/{ticket_id}", response_model=TicketRead, tags=["tickets"])
async def get_ticket_endpoint (ticket_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
  ticket = await service.get_ticket(db, ticket_id)
  if ticket is None:
    return HTTPException(status_code=404, detail="Ticket not found")
  return ticket

@router.patch("/tickets/{ticket_id}", response_model=TicketRead, tags=["tickets"])
async def patch_ticket_endpoint (ticket_id: uuid.UUID, data: TicketUpdate, db: AsyncSession = Depends(get_db)):
  ticket = await service.get_ticket(db, ticket_id)
  if ticket is None:
    return HTTPException(status_code=404, detail="Ticket not found")
  return service.update_ticket(db, ticket, data)

@router.delete("/tickets/{ticket_id}", status_code=http_status.HTTP_204_NO_CONTENT, tags=["tickets"])
async def patch_ticket_endpoint (ticket_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
  ticket = await service.get_ticket(db, ticket_id)
  if ticket is None:
    return HTTPException(status_code=404, detail="Ticket not found")
  return service.delete_ticket(db, ticket)
