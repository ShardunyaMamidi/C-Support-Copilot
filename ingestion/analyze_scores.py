# one-off data analysis script — not part of the ingestion pipeline itself.
# samples a bounded slice of the stream and reports the real score distribution
# for niche-tagged questions, so we can pick a min_score threshold grounded in
# actual data instead of guessing from scores seen across the whole dataset.

import statistics
from datasets import load_dataset
from ingestion.load_stackoverflow import NICHE

SAMPLE_SIZE = 2_000_000
FULL_DATASET_SIZE = 58_300_000

CANDIDATE_THRESHOLDS = [1, 5, 10, 20, 50, 100, 250, 500]


def analyze():
  ds = load_dataset("mikex86/stackoverflow-posts", split="train", streaming=True).take(SAMPLE_SIZE)

  scores_with_accepted = []
  niche_questions_total = 0
  scanned = 0

  for row in ds:
    scanned += 1

    if scanned % 200_000 == 0:
      print(f"scanned {scanned}/{SAMPLE_SIZE} rows, niche questions found so far: {niche_questions_total}", flush=True)

    if row.get("PostTypeId") != 1:
      continue

    tags = set(row.get("Tags") or [])
    if not (tags & NICHE):
      continue

    niche_questions_total += 1
    if row.get("AcceptedAnswerId") is not None:
      scores_with_accepted.append(row.get("Score") or 0)

  print(f"\nscanned {scanned} rows total")
  print(f"niche-tagged questions found: {niche_questions_total}")
  print(f"of those, with an accepted answer: {len(scores_with_accepted)}")

  if not scores_with_accepted:
    print("no niche questions with accepted answers found in this sample.")
    return

  sorted_scores = sorted(scores_with_accepted)
  print("\nscore distribution (niche questions WITH an accepted answer):")
  print(f"  min: {sorted_scores[0]}")
  print(f"  max: {sorted_scores[-1]}")
  print(f"  median: {statistics.median(sorted_scores)}")
  print(f"  mean: {statistics.mean(sorted_scores):.1f}")

  scale_factor = FULL_DATASET_SIZE / SAMPLE_SIZE
  print(f"\nthreshold breakdown, extrapolated to the full {FULL_DATASET_SIZE:,} row dataset (scale factor {scale_factor:.1f}x):")
  for threshold in CANDIDATE_THRESHOLDS:
    count_in_sample = sum(1 for s in sorted_scores if s >= threshold)
    projected_full = count_in_sample * scale_factor
    print(f"  >= {threshold:>4}: {count_in_sample:>6} in sample  ->  ~{projected_full:,.0f} projected across full dataset")


if __name__ == "__main__":
  analyze()
