import uuid
import enum
from typing import Optional
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

class Base(DeclarativeBase):
  pass

class TicketStatus(str, enum.Enum):
  OPEN = "open"
  IN_PROGRESS = "in_progress",
  RESOLVED = "resolved",
  ESCALATED = "escalated"

class TicketPriority(str, enum.Enum):
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"

class Customer(Base):
  __tablename__ = "customers"

  id: Mapped[uuid.uuid4] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
  name: Mapped[str] = mapped_column(String(255))
  email: Mapped[str] = mapped_column(String(255), unique=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  tickets: Mapped[list["Ticket"]] = relationship(back_populates="customer")

class Ticket(Base):
  __tablename__ = "tickets"

  id: Mapped[uuid.uuid4] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
  customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("customers.id"))
  subject: Mapped[str] = mapped_column(String(255))
  body: Mapped[str] = mapped_column(Text)
  status: Mapped[TicketStatus] = mapped_column(SqlEnum(TicketStatus), default=TicketStatus.OPEN)
  priority: Mapped[TicketPriority] = mapped_column(SqlEnum(TicketPriority), default=TicketPriority.MEDIUM)
  category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
  ai_draft: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  customer: Mapped["Customer"] = relationship(back_populates="tickets")

class KBArticle(Base):
  __tablename__ = "kb_articles"

  id: Mapped[uuid.uuid4] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
  title: Mapped[str] = mapped_column(String(255))
  body: Mapped[str] = mapped_column(Text)
  source_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
  tags: Mapped[list[str]] = mapped_column(ARRAY(String(50)), default=list)
  qdrant_synced: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

