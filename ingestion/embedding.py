import hashlib
import json
import time
from pathlib import Path

from google import genai
from google.genai import types

from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

CACHE_PATH = Path("ingestion/embedding_cache.jsonl")
RATE_LIMIT_SLEEP_SECONDS = 0.5

def load_cache() -> dict[str, list[float]]:
  cache = {}
  if CACHE_PATH.exists():
    with CACHE_PATH.open() as f:
      for line in f:
        entry = json.loads(line)
        cache[entry["hash"]] = entry["embedding"]

  return cache

def _hash_text(text: str) -> str:
  return hashlib.sha256(text.encode("utf-8")).hexdigest()

def embed_document(text: str, cache: dict[str, list[float]]) -> list[float]:
  key = _hash_text(text)
  if key in cache:
    return cache[key]

  result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768),
  )
  embedding = result.embeddings[0].values
  cache[key] = embedding

  with CACHE_PATH.open("a") as f:
    f.write(json.dumps({
      "hash": key, "embedding": embedding
    }) + "\n")

  time.sleep(RATE_LIMIT_SLEEP_SECONDS)
  return embedding
