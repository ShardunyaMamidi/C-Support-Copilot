from fastapi import FastAPI
from app.modules.crud import router as crud_router

app = FastAPI(title="C Support Copilot")
app.include_router(crud_router)