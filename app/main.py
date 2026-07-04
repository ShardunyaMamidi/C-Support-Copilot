from fastapi import FastAPI
from app.modules.crud.router import crud_router

app = FastAPI(title="C Support Copilot")
app.include_router(crud_router)