import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.modules.crud.models import TicketPriority, TicketStatus

# Ticket request and response

class TicketCreate(BaseModel):
  customer_id: uuid.UUID
  subject: str
  body: str
  priority: TicketPriority = TicketPriority.MEDIUM

class TicketUpdate(BaseModel):
  subject: Optional[str] = None
  body: Optional[str] = None
  status: Optional[TicketStatus] = None
  priority: Optional[TicketPriority] = None
  category: Optional[str] = None
  ai_draft: Optional[str] = None

class TicketRead(BaseModel):
  id: uuid.UUID
  customer_id: uuid.UUID
  subject: str
  body: str
  status: TicketStatus
  priority: TicketPriority
  category: Optional[str]
  ai_draft: Optional[str]
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

# Customer request and response

class CustomerCreate(BaseModel):
  name: str
  email: str

class CustomerUpdate(BaseModel):
  name: Optional[str] = None
  email: Optional[str] = None

class CustomerRead(BaseModel):
  id: uuid.UUID
  name: str
  email: str
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)

# Knowledge Base request and response

class KBArticleCreate(BaseModel):
  title: str
  body: str
  source_url: Optional[str] = None
  tags: list[str] = []

class KBArticleUpdate(BaseModel):
  title: Optional[str] = None
  body: Optional[str] = None
  source_url: Optional[str] = None
  tags: Optional[list[str]] = None

class KBArticleRead(BaseModel):
  id: uuid.UUID
  title: str
  body: str
  source_url: Optional[str] = None
  qdrant_synced: bool
  created_at: datetime
  tags: Optional[list[str]] = None

  model_config = ConfigDict(from_attributes=True)

