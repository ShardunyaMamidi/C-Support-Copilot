from fastapi import FastAPI
from app.modules.crud.router import crud_router
from app.modules.rag.router import rag_router
from app.modules.agents.router import agent_router

app = FastAPI(title="C Support Copilot")
app.include_router(crud_router)
app.include_router(rag_router, prefix="/rag")
app.include_router(agent_router, prefix="/agent")