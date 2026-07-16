from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from app.modules.rag.retriever import retrieve_chunks
from app.modules.agents.llm import get_llm
from app.modules.agents.schemas import TriageResult
from app.modules.agents.prompts import TRIAGE_PROMPT, ANSWER_PROMPT

def format_sources(chunks: list[dict]) -> str:
  return "\n\n".join(
    f"[{c["source_url"]}]\n{c["chunk_text"]}" for c in chunks
  )

async def get_context(x: dict) -> str:
  chunks = await retrieve_chunks(x["question"])
  return format_sources(chunks)

def build_rag_chain(provider="gemini"):
  llm = get_llm(provider=provider)
  return (
    {
      "context": RunnableLambda(get_context),
      "question": lambda x: x["question"]
    } 
    | ANSWER_PROMPT 
    | llm 
    | StrOutputParser()
  )

def build_triage_chain(provider="gemini"):
  llm = get_llm(provider=provider).with_structured_output(TriageResult)
  return TRIAGE_PROMPT | llm