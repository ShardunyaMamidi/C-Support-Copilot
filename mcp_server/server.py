"""MCP server for the C/embedded support copilot.

Wraps the FastAPI app's capabilities as MCP tools. Each tool makes an HTTP
call into the FastAPI app and returns a typed result to the MCP client
(Claude Code over stdio, or the LangGraph agents over HTTP/SSE).
"""

from typing import Literal

import httpx
from mcp.server.fastmcp import FastMCP

from config import settings
from schemas import CustomerRead, KBSearchResult, TicketDetail, TicketSummary

# host/port only matter when running over SSE/HTTP (Docker Compose). Bind
# 0.0.0.0 so the agent container can reach it; the port comes from config.
# For the stdio demo (Claude Code) these are simply ignored.
mcp = FastMCP("c-support-copilot", host="0.0.0.0", port=settings.mcp_port)

APP_URL = settings.app_url


@mcp.tool()
async def search_kb(query: str, top_k: int = 5) -> list[KBSearchResult]:
    """Search the C/embedded systems knowledge base for relevant Q&A.
    Use this to find answers to developer questions about C, embedded,
    STM32, ARM, memory management, pointers, or toolchain issues.
    Returns ranked articles with title, source URL, a text snippet, and a
    relevance score."""
    async with httpx.AsyncClient() as c:
        r = await c.post(
            f"{APP_URL}/rag/search", json={"query": query, "top_k": top_k}
        )
        r.raise_for_status()
        return [KBSearchResult(**hit) for hit in r.json()]


@mcp.tool()
async def create_ticket(
    customer_id: str,
    subject: str,
    body: str,
    priority: Literal["low", "medium", "high"] = "medium",
) -> TicketDetail:
    """Create a new support ticket for a customer.
    Use when a developer reports a new problem that needs tracking. Requires
    the customer's id (look one up with get_customer if you only have a name).
    Returns the created ticket, including its new id and status."""
    async with httpx.AsyncClient() as c:
        r = await c.post(
            f"{APP_URL}/tickets",
            json={
                "customer_id": customer_id,
                "subject": subject,
                "body": body,
                "priority": priority,
            },
        )
        r.raise_for_status()
        return TicketDetail(**r.json())


@mcp.tool()
async def get_ticket(ticket_id: str) -> TicketDetail:
    """Fetch a single support ticket by its id.
    Use to check the current status, priority, subject, body, category, and
    any AI-drafted reply for an existing ticket. Returns the full ticket
    record, or raises if no ticket has that id."""
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{APP_URL}/tickets/{ticket_id}")
        r.raise_for_status()
        return TicketDetail(**r.json())


@mcp.tool()
async def list_tickets(
    status: Literal["open", "in_progress", "resolved", "escalated"] | None = None,
    limit: int = 20,
) -> list[TicketSummary]:
    """List support tickets, most useful for finding a ticket's id before
    acting on it. Optionally filter by status (open, in_progress, resolved,
    escalated). Use this to answer questions like "which tickets are still
    open?" or to locate the ticket a user is describing before calling
    get_ticket, update_ticket_status, or escalate.
    Returns a compact summary per ticket (id, subject, status, priority,
    customer_id, created_at) — call get_ticket for the full body."""
    params: dict = {"limit": limit}
    if status is not None:
        params["status"] = status
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{APP_URL}/tickets", params=params)
        r.raise_for_status()
        return [TicketSummary(**ticket) for ticket in r.json()]


@mcp.tool()
async def update_ticket_status(
    ticket_id: str,
    status: Literal["open", "in_progress", "resolved", "escalated"],
) -> TicketDetail:
    """Move a ticket to a new lifecycle status.
    Valid statuses: open, in_progress, resolved, escalated. Use as a developer
    works a ticket (e.g. mark in_progress when starting, resolved when the fix
    is delivered). To flag for senior human review, prefer the dedicated
    `escalate` tool. Returns the updated ticket record."""
    async with httpx.AsyncClient() as c:
        r = await c.patch(
            f"{APP_URL}/tickets/{ticket_id}", json={"status": status}
        )
        r.raise_for_status()
        return TicketDetail(**r.json())


@mcp.tool()
async def escalate(ticket_id: str) -> TicketDetail:
    """Flag a ticket for senior human review by setting its status to escalated.
    Use when a problem is beyond automated/first-line handling — safety-critical
    embedded bugs, hardware faults, or anything the AI is not confident about.
    This is a one-way signal that a human must take over. Returns the updated
    ticket record."""
    async with httpx.AsyncClient() as c:
        r = await c.patch(
            f"{APP_URL}/tickets/{ticket_id}", json={"status": "escalated"}
        )
        r.raise_for_status()
        return TicketDetail(**r.json())


@mcp.tool()
async def get_customer(customer_id: str) -> CustomerRead:
    """Look up a customer by id.
    Use to retrieve a customer's name, email, and signup date — for example
    before creating a ticket on their behalf, or to confirm who a ticket
    belongs to. Returns the customer record, or raises if the id is unknown."""
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{APP_URL}/customers/{customer_id}")
        r.raise_for_status()
        return CustomerRead(**r.json())


if __name__ == "__main__":
    # Transport is driven by config: "stdio" for the Claude Code demo (default),
    # "sse" for the agent service inside Docker Compose. Set MCP_TRANSPORT in the
    # environment to switch — no CLI flags to parse.
    mcp.run(transport=settings.mcp_transport)
