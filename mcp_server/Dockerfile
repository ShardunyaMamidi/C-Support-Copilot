FROM python:3.11-slim

WORKDIR /code

COPY mcp_server/requirements.txt .

RUN pip install -r requirements.txt

COPY mcp_server/ ./

# Transport is chosen at runtime via the MCP_TRANSPORT env var (see config.py).
# Compose sets it to "sse"; the default stdio mode is for the local Claude Code demo.
CMD ["python", "server.py"]
