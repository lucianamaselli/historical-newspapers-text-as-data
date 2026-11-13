"""Summarize the coverage and repeated records in an exploratory corpus."""

import argparse
from collections import Counter
import csv
from pathlib import Path


def read_records(path):
    """Yield records with validated publication years."""
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"year", "clean_text"}
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        for row in reader:
            try:
                year = int(row["year"] or "")
            except ValueError as error:
                raise ValueError(f"Invalid year at CSV line {reader.line_num}") from error
            if not 1840 <= year <= 1923:
                raise ValueError(f"Year outside 1840–1923 at CSV line {reader.line_num}")
            yield year, row


def audit(path):
    decades = Counter()
    states = Counter()
    texts = Counter()
    article_ids = Counter()
    source_blocks = Counter()
    blank_texts = 0
    for year, row in read_records(path):
        decades[year // 10 * 10] += 1
        states[(row.get("state") or "").strip() or "(missing)"] += 1
        cleaned_text = (row["clean_text"] or "").strip()
        if cleaned_text:
            texts[cleaned_text] += 1
        else:
            blank_texts += 1
        article_id = (row.get("full_article_id") or "").strip()
        if article_id:
            article_ids[article_id] += 1
        if row.get("json_path") and row.get("block_id"):
            source_blocks[row["json_path"], row["block_id"]] += 1

    print(f"Records: {sum(decades.values()):,}")
    print(f"Blank cleaned texts: {blank_texts:,}")
    for label, counts in (
        ("nonblank cleaned text", texts),
        ("article ID", article_ids),
        ("source path and block ID", source_blocks),
    ):
        covered = sum(counts.values())
        print(f"Repeated {label}: {covered - len(counts):,} extra rows among {covered:,}")
    print("\nRecords by decade:")
    for decade, count in sorted(decades.items()):
        print(f"  {decade}: {count:,}")
    print("\nTop ten states by record count:")
    for state, count in states.most_common(10):
        print(f"  {state}: {count:,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    audit(args.csv)
