"""Response models for the MCP tools.

These mirror the shapes the FastAPI app returns over HTTP. They are declared
here (not imported from `app/`) on purpose: `mcp_server` is a separate service
with its own dependencies and container, so it depends on the API's *contract*,
not its code. Typing the tool returns gives us validation of what the API sent
back and lets FastMCP publish an output schema to the MCP client.
"""

from datetime import datetime
from pydantic import BaseModel


class KBSearchResult(BaseModel):
    """One ranked hit from the knowledge-base semantic search."""

    title: str
    source_url: str | None = None
    chunk_text: str
    score: float


class CustomerRead(BaseModel):
    """A customer record."""

    id: str
    name: str
    email: str
    created_at: datetime


class TicketSummary(BaseModel):
    """Lightweight ticket view for discovery/listing.

    Deliberately omits the heavy `body` and `ai_draft` fields so a list of
    tickets stays compact in the model's context. Call `get_ticket` for the
    full record.
    """

    id: str
    subject: str
    status: str
    priority: str
    customer_id: str
    created_at: datetime


class TicketDetail(TicketSummary):
    """Full ticket record, including the fields omitted from TicketSummary."""

    body: str
    category: str | None = None
    ai_draft: str | None = None
    updated_at: datetime
