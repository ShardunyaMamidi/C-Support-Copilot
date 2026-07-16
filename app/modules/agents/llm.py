from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def get_llm(provider: str = "gemini"):
  if provider == "gemini":
    return ChatGoogleGenerativeAI(
      model="gemini-3.1-flash-lite",
      temperature=0,
      google_api_key=settings.gemini_api_key
    )
  return ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=settings.gemini_api_key
  )