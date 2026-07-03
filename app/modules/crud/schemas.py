import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.modules.crud.models import TicketPriority, TicketStatus

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
