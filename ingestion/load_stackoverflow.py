# responsible for ingestion/rag

from datasets import load_dataset
from app.database import SessionLocal
from app.modules.crud.models import KBArticle

NICHE = {"c", "c++", "assembly", "embedded", "microcontroller", "arm", "stm32", "memory-management", "pointers", "gcc"}

# data-processing as each row could be a question or answer
# if postTypeId == 1: question and 2 is an answer
# answerId tells which row is the answer for that question

def is_target_question(row: dict, min_score: int) -> bool:
  if row.get("PostTypeId") != 1:
    return False

  tags = set(row.get("Tags") or [])
  score = row.get("Score") or 0
  return bool(tags & NICHE) and score >= min_score and row.get("AcceptedAnswerId") is not None

# single forward pass: buffers questions awaiting their accepted answer, and
# pairs+writes them to postgres in batches as soon as both halves are seen,
# instead of scanning the whole stream twice and writing everything at the end
async def fetch_and_save(limit: int = 15000, min_score: int = 10, batch_size: int = 500, max_text_mb: int = 400) -> int:
  ds = load_dataset("mikex86/stackoverflow-posts", split="train", streaming=True)
  max_text_bytes = max_text_mb * 1024 * 1024

  # map with key as answerId and the value being the entire question obj,
  # holding questions that haven't found their answer row yet
  pending = {}
  batch = []
  saved = 0
  total_bytes = 0
  scanned = 0

  for row in ds:
    scanned += 1
    post_type = row.get("PostTypeId")

    if post_type == 1 and is_target_question(row, min_score):
      pending[row["AcceptedAnswerId"]] = {
        "question_id": row["Id"],
        "title": row["Title"],
        "body": row["Body"],
        "tags": row["Tags"],
        "score": row["Score"],
      }
    elif post_type == 2 and row["Id"] in pending:
      question = pending.pop(row["Id"])
      answer_body = row["Body"]
      batch.append({**question, "answer_body": answer_body})
      total_bytes += len(question["body"].encode("utf-8")) + len(answer_body.encode("utf-8"))

    if scanned % 50000 == 0:
      print(f"scanned {scanned} rows, saved {saved} articles so far, pending {len(pending)}, ~{total_bytes / 1024 / 1024:.1f} MB of text", flush=True)

    if len(batch) >= batch_size:
      await save_pairs_to_postgres(batch)
      saved += len(batch)
      print(f"saved {saved}/{limit} articles (~{total_bytes / 1024 / 1024:.1f} MB of text written so far)", flush=True)
      batch = []

    if saved >= limit or total_bytes >= max_text_bytes:
      break

  if batch:
    await save_pairs_to_postgres(batch)
    saved += len(batch)

  hit_cap = total_bytes >= max_text_bytes
  print(f"done. scanned {scanned} rows, saved {saved} articles, ~{total_bytes / 1024 / 1024:.1f} MB of raw text total"
        + (f" (stopped early: hit the {max_text_mb} MB text cap)" if hit_cap else ""), flush=True)
  return saved

def build_article_body(question_body: str, answer_body: str) -> str:
  return f"{question_body}\n\n## Resolution\n\n{answer_body}"

async def save_pairs_to_postgres(pairs: list[dict]) -> list[KBArticle]:
  articles = [
    KBArticle(
      title=pair["title"],
      body=build_article_body(pair["body"], pair["answer_body"]),
      source_url=f"https://stackoverflow.com/questions/{pair['question_id']}",
      qdrant_synced=False,
      tags=pair["tags"]
    )
    for pair in pairs
  ]

  async with SessionLocal() as session:
    session.add_all(articles)
    await session.commit()

  return articles


if __name__ == "__main__":
  import asyncio

  asyncio.run(fetch_and_save())